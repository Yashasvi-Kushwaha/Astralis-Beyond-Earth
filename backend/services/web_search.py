import os
from dotenv import load_dotenv
from tavily import TavilyClient

load_dotenv()


class WebSearch:

    def __init__(self):
        api_key = os.getenv("TAVILY_API_KEY")

        if not api_key:
            raise ValueError("TAVILY_API_KEY not found")

        self.client = TavilyClient(api_key=api_key)

    def search(self, query: str):

        response = self.client.search(
            query=query,
            search_depth="advanced",
            max_results=5
        )

        return response["results"]