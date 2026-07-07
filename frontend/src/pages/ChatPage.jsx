import { useState, useEffect } from "react";
import { useLocation } from "react-router-dom";

import Navbar from "../components/Navbar";
import Sidebar from "../components/Sidebar";
import ChatWindow from "../components/ChatWindow";
import ChatInput from "../components/ChatInput";

import API from "../services/api";

function generateTitle(question) {

    const stopWords = [
        "what",
        "is",
        "are",
        "the",
        "a",
        "an",
        "tell",
        "me",
        "about",
        "explain",
        "please",
        "how",
        "does",
        "do",
        "can",
        "could",
        "would",
        "of",
        "in",
        "for",
        "to"
    ];

    const words = question
        .toLowerCase()
        .replace(/[^\w\s]/g, "")
        .split(" ")
        .filter(word => !stopWords.includes(word));

    const title = words
        .slice(0, 4)
        .join(" ")
        .replace(/\b\w/g, c => c.toUpperCase());

    return title || "New Chat";
}

function App() {

    const location = useLocation();

    const [messages, setMessages] = useState([]);

    const [chats, setChats] = useState([]);

    const [sessionId, setSessionId] = useState(
        crypto.randomUUID()
    );

    const [loading, setLoading] = useState(false);
// -----------------------------
// Start New Chat
// -----------------------------
const newChat = () => {

    if (messages.length > 0) {

        setChats(prev => {

            const exists = prev.find(
                chat => chat.id === sessionId
            );

            if (exists) {

                return prev.map(chat =>

                    chat.id === sessionId
                        ? {
                            ...chat,
                            messages: [...messages]
                        }
                        : chat

                );

            }

            return [

                {
                    id: sessionId,
                    title:
                        generateTitle(
                            messages.find(
                                m => m.sender === "user"
                            )?.text || "New Chat"
                        ),
                    messages: [...messages]
                },

                ...prev

            ];

        });

    }

    setMessages([]);

    setLoading(false);

    setSessionId(
        crypto.randomUUID()
    );

};


// -----------------------------
// Send Message
// -----------------------------
const sendMessage = async (question) => {

    if (!question.trim()) return;

    const userMessage = {

        sender: "user",

        text: question

    };

    const updatedMessages = [

        ...messages,

        userMessage

    ];

    setMessages(updatedMessages);

    setLoading(true);

    try {

        const res = await API.post(

            "/chat",

            {

                session_id: sessionId,

                message: question

            }

        );

        const botMessage = {

            sender: "bot",

            text: res.data.response

        };

        const finalMessages = [

            ...updatedMessages,

            botMessage

        ];

        setMessages(finalMessages);

        setLoading(false);

        setChats(prev => {

            const exists = prev.find(
                chat => chat.id === sessionId
            );

            if (exists) {

                return prev.map(chat =>

                    chat.id === sessionId
                        ? {
                            ...chat,
                            messages: finalMessages
                        }
                        : chat

                );

            }

            return [

                {

                    id: sessionId,

                    title: generateTitle(question),

                    messages: finalMessages

                },

                ...prev

            ];

        });

    }

    catch (err) {

        setLoading(false);

        const botMessage = {

            sender: "bot",

            text:
                JSON.stringify(
                    err.response?.data ||
                    err.message
                )

        };

        const finalMessages = [

            ...updatedMessages,

            botMessage

        ];

        setMessages(finalMessages);

    }

};
// -----------------------------
// Auto-send topic from Landing Page
// -----------------------------
useEffect(() => {

    if (!location.state?.question) return;

    sendMessage(location.state.question);

    // Prevent sending again if user refreshes
    window.history.replaceState({}, document.title);

}, []);


// -----------------------------
// Open Previous Chat
// -----------------------------
const selectChat = (chat) => {

    setSessionId(chat.id);

    setMessages([...chat.messages]);

    setLoading(false);

};


// -----------------------------
// Delete Chat
// -----------------------------
const deleteChat = (id) => {

    setChats(prev =>
        prev.filter(chat => chat.id !== id)
    );

    // If currently opened chat is deleted,
    // create a fresh session.
    if (sessionId === id) {

        setMessages([]);

        setLoading(false);

        setSessionId(
            crypto.randomUUID()
        );

    }

};
return (

    <div className="h-screen w-screen flex flex-col bg-slate-950 text-white">

        <Navbar />

        <div className="flex flex-1 overflow-hidden">

            <Sidebar

                chats={chats}

                onNewChat={newChat}

                onSelectChat={selectChat}

                onDeleteChat={deleteChat}

            />

            <div className="flex flex-col flex-1">

                <ChatWindow

                    messages={messages}

                    loading={loading}

                />

                <ChatInput

                    onSend={sendMessage}

                />

            </div>

        </div>

    </div>

);

}

export default App;