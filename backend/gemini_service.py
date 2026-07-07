import os
import time

from dotenv import load_dotenv
from google import genai
from google.genai.errors import APIError

from rag.pipeline import vector_store
from rag.retriever import Retriever
from services.web_search import WebSearch

load_dotenv()


class GeminiService:

    def __init__(self):

        self.api_key = os.getenv("GEMINI_API_KEY")

        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found")

        self.client = genai.Client(api_key=self.api_key)

        self.model_name = os.getenv(
            "GEMINI_MODEL",
            "gemini-2.5-flash"
        )

        self.sessions = {}

        self.retriever = Retriever()

        self.web_search = WebSearch()

    def generate_with_retry(self, prompt):

        for attempt in range(3):

            try:

                return self.client.models.generate_content(
                    model=self.model_name,
                    contents=prompt
                )

            except APIError as e:

                error = str(e).lower()

                if (
                    "high demand" in error
                    or "503" in error
                    or "unavailable" in error
                ):

                    print(
                        f"Gemini busy... Retry {attempt + 1}/3"
                    )

                    time.sleep(3)

                else:
                    raise

        raise RuntimeError(
            "Gemini servers are temporarily unavailable."
        )

    def chat(self, session_id: str, message: str) -> str:

        try:

            # -----------------------------
            # Conversation Memory
            # -----------------------------
            if session_id not in self.sessions:
                self.sessions[session_id] = []

            history = self.sessions[session_id]
            history.append(f"User: {message}")

            # -----------------------------
            # Casual Conversation Handling
            # -----------------------------
            msg = message.lower().strip()

            greetings = {
                "hi",
                "hello",
                "hey",
                "good morning",
                "good afternoon",
                "good evening"
            }

            if msg in greetings:

                answer = (
                    "Hello! 👋 I'm Astralis.\n\n"
                    "I can answer astronomy questions, explain research papers, "
                    "search the web when needed, and summarize uploaded PDFs."
                )

                history.append(f"Astralis: {answer}")
                return answer

            if msg in ["thanks", "thank you"]:

                answer = "You're welcome! 🚀"

                history.append(f"Astralis: {answer}")
                return answer

            if msg in ["bye", "goodbye"]:

                answer = "Goodbye! Clear skies. 🌌"

                history.append(f"Astralis: {answer}")
                return answer

            if msg in ["who are you", "what are you"]:

                answer = (
                    "I'm Astralis, an AI Astronomy Research Assistant.\n\n"
                    "I answer astronomy questions using research papers in my knowledge base "
                    "and search the web whenever additional information is needed."
                )

                history.append(f"Astralis: {answer}")
                return answer

            if msg in ["help", "what can you do"]:

                answer = (
                    "I can help you with:\n\n"
                    "• Astronomy questions\n"
                    "• Black holes, stars, galaxies and cosmology\n"
                    "• Explaining scientific concepts\n"
                    "• Searching research papers\n"
                    "• Searching the web when necessary\n"
                    "• Summarizing uploaded PDFs\n"
                    "• Answering questions from your uploaded papers"
                )

                history.append(f"Astralis: {answer}")
                return answer

            # -----------------------------
            # Retrieve
            # -----------------------------
            retrieved = self.retriever.retrieve(
                message,
                k=5
            )

            print("\n========== Retrieval ==========")

            for item in retrieved:

                print(
                    f"Score={item['score']:.2f}",
                    f"Distance={item['distance']:.2f}",
                    item["metadata"]["paper"],
                    item["metadata"]["page"]
                )

            print("===============================\n")

            use_web = False

            if len(retrieved) == 0:

                print("No relevant chunks found.")
                use_web = True

            elif retrieved[0]["score"] < 1.5:

                print(
                    f"Low reranker score: {retrieved[0]['score']:.2f}"
                )

                use_web = True

            sources = []

        # -----------------------------
        # Local Papers
        # -----------------------------
            if not use_web:

                retrieved_chunks = [
                    item["metadata"]
                    for item in retrieved
                ]

                rag_context = "\n\n".join(
                    chunk["text"]
                    for chunk in retrieved_chunks
                )

                seen = set()

                for chunk in retrieved_chunks:

                    source = (
                        f'{chunk["paper"]} '
                        f'(Page {chunk["page"]})'
                    )

                    if source not in seen:

                        seen.add(source)
                        sources.append(source)

            # -----------------------------
            # Tavily
            # -----------------------------
            else:

                print("Searching Tavily...")

                web_results = self.web_search.search(
                    message
                )

                rag_context = "\n\n".join(
                    result["content"]
                    for result in web_results
                )

                sources = [
                    result["url"]
                    for result in web_results
                ]

            # -----------------------------
            # Prompt
            # -----------------------------
            chat_history = "\n".join(history[-10:])

            prompt = f"""
You are Astralis, an AI Astronomy Research Assistant.

Rules:

1. If the user greets you (Hello, Hi, Hey, Good morning, etc.), respond naturally and do NOT search the context.

2. If the user asks casual questions like:
   - Who are you?
   - What can you do?
   - Thank you
   - Bye

   answer naturally.

3. For astronomy questions:
   - Use ONLY the supplied context.
   - Never invent facts.
   - If the context is insufficient, clearly state that.

4. For every astronomy answer use EXACTLY this format.

Definition:
A concise explanation in 2–4 sentences.

Key Points:
• point 1
• point 2
• point 3

References:
Do not write references yourself.




=========================
Context
=========================

{rag_context}

=========================
Conversation
=========================

{chat_history}

=========================
User Question
=========================

{message}
"""

            response = self.generate_with_retry(prompt)

            answer = response.text

            # -----------------------------
            # Automatic fallback
            # -----------------------------
            fallback_phrases = [

                "could not find",
                "does not contain",
                "does not provide",
                "does not answer",
                "not available",
                "not present",
                "insufficient",
                "cannot answer",
                "cannot determine",
                "the context does not",
                "the provided context",
                "based on the supplied information",
                "based solely on the supplied information",
                "does not provide a direct definition",
                "the context is insufficient",
                "cannot be determined from the context"

            ]

            if (
                not use_web
                and any(
                    phrase in answer.lower()
                    for phrase in fallback_phrases
                )
            ):

                print("Gemini says context is insufficient.")
                print("Searching Tavily...")

                web_results = self.web_search.search(
                    message
                )

                web_context = "\n\n".join(
                    result["content"]
                    for result in web_results
                )

                prompt = f"""
You are Astralis.

Answer the question using ONLY the following web search results.

=========================
Web Results
=========================

{web_context}

=========================
User Question
=========================

{message}
"""

                response = self.generate_with_retry(
                    prompt
                )

                answer = response.text

                sources = [
                    result["url"]
                    for result in web_results
                ]

                use_web = True

            history.append(
                f"Astralis: {answer}"
            )

            if sources:

                if use_web:
                    answer += "\n\n🌐 Web Sources:\n"
                else:
                    answer += "\n\n📚 Research Papers:\n"

                for source in sources:
                    answer += f"• {source}\n"

            return answer

        except APIError as e:

            raise RuntimeError(
                f"Gemini API Error: {e.message}"
            ) from e

        except Exception as e:

            raise RuntimeError(str(e)) from e