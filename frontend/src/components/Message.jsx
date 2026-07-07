import ReactMarkdown from "react-markdown";
import logo from "../assets/astralis-logo.png";

function Message({ sender, text }) {

    const isUser = sender === "user";

    return (

        <div
            className={`flex mb-6 ${
                isUser ? "justify-end" : "justify-start"
            }`}
        >

            <div
                className={`flex gap-3 max-w-5xl ${
                    isUser ? "flex-row-reverse" : ""
                }`}
            >

                {/* Avatar */}

                <div
                    className={`w-11 h-11 rounded-full flex items-center justify-center shrink-0 overflow-hidden ${
                        isUser
                            ? "bg-blue-600"
                            : "bg-slate-900 border border-violet-500 shadow-[0_0_20px_rgba(168,85,247,0.5)]"
                    }`}
                >

                    {isUser ? (

                        <span className="text-lg">👤</span>

                    ) : (

                        <img
                            src={logo}
                            alt="Astralis"
                            className="w-9 h-9 object-contain"
                        />

                    )}

                </div>

                {/* Message Bubble */}

                <div
                    className={`rounded-2xl px-5 py-4 shadow-lg ${
                        isUser
                            ? "bg-blue-600 text-white"
                            : "bg-slate-800 text-slate-100 border border-slate-700"
                    }`}
                >

                    <div className="text-sm font-semibold mb-2 opacity-80">

                        {isUser ? "You" : "Astralis"}

                    </div>

                    <div className="prose prose-invert max-w-none leading-7">

                        <ReactMarkdown>
                            {text}
                        </ReactMarkdown>

                    </div>

                </div>

            </div>

        </div>

    );

}

export default Message;