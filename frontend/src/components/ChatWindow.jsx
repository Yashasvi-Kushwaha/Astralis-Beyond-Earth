import { useEffect, useRef } from "react";
import Message from "./Message";

function ChatWindow({ messages, loading }) {

    const bottomRef = useRef(null);

    useEffect(() => {

        bottomRef.current?.scrollIntoView({
            behavior: "HARSH"
        });

    }, [messages, loading]);

    return (

        <div className="flex-1 overflow-y-auto p-6">

            {messages.length === 0 ? (

                <div className="flex flex-col items-center justify-center h-full text-center text-slate-400">

                    <h1 className="text-7xl mb-6">🚀</h1>

                    <h2 className="text-5xl font-bold text-white">

                        Astralis

                    </h2>

                    <p className="mt-3 text-xl">

                        AI Astronomy Research Assistant

                    </p>

                    <div className="mt-10 space-y-2 text-lg">

                        <p>⭐ Black Holes
                      ⭐ Galaxies
                        ⭐ Space Exploration
                      ⭐ Cosmology
                        ⭐ Exoplanets</p>

                    </div>

                    <p className="mt-10 text-slate-500">

                        UPLOAD RESEARCH PAPERS OR ASK ANY ASTRONOMY QUESTIONS!

                    </p>

                </div>

            ) : (

                <>
                    {messages.map((msg, index) => (

                        <Message
                            key={index}
                            sender={msg.sender}
                            text={msg.text}
                        />

                    ))}

                    {loading && (

                        <div className="flex items-center gap-3 mt-6">

                            <div className="w-3 h-3 bg-cyan-400 rounded-full animate-bounce"></div>
                            <div className="w-3 h-3 bg-cyan-400 rounded-full animate-bounce delay-100"></div>
                            <div className="w-3 h-3 bg-cyan-400 rounded-full animate-bounce delay-200"></div>

                            <span className="text-slate-400">

                                Astralis is thinking...

                            </span>

                        </div>

                    )}

                    <div ref={bottomRef}></div>

                </>

            )}

        </div>

    );

}

export default ChatWindow;