import { FaPaperPlane } from "react-icons/fa";
import { useState, useRef } from "react";
import API from "../services/api";


function ChatInput({ onSend }) {

    const [message, setMessage] = useState("");

    const fileRef = useRef();

    const handleSend = () => {

        if (!message.trim()) return;

        onSend(message);

        setMessage("");

    };

    const handleUpload = async (e) => {

        const file = e.target.files[0];

        if (!file) return;

        try {

            const formData = new FormData();

            formData.append("file", file);

            const res = await API.post(
                "/upload",
                formData,
                {
                    headers: {
                        "Content-Type": "multipart/form-data"
                    }
                }
            );

            // Show upload confirmation
            onSend(`📄 Uploaded: ${file.name}`);

            // Show summary returned by backend
            onSend(res.data.summary);

        } catch (err) {

            console.log(err);

            alert("Failed to upload PDF.");

        }

    };

    return (

        <div className="border-t border-slate-700 p-5 flex gap-3">

            <input
                value={message}
                onChange={(e) => setMessage(e.target.value)}
                onKeyDown={(e) => {
                    if (e.key === "Enter") handleSend();
                }}
                placeholder="Ask Astralis anything..."
                className="flex-1 bg-slate-800 rounded-lg px-4 py-3 outline-none"
            />

            <input
                type="file"
                accept=".pdf"
                ref={fileRef}
                hidden
                onChange={handleUpload}
            />

            <button
                onClick={() => fileRef.current.click()}
                className="bg-violet-600 hover:bg-violet-700 px-4 rounded-lg"
            >
                UPLOAD PDF
            </button>

            <button
                onClick={handleSend}
                className="bg-blue-600 hover:bg-blue-700 px-5 rounded-lg"
            >
                <FaPaperPlane />
            </button>

        </div>

    );

}

export default ChatInput;