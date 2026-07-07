import { FaPlus, FaHistory, FaTrash } from "react-icons/fa";

function Sidebar({

    chats,

    onNewChat,

    onSelectChat,

    onDeleteChat

}) {

    return (

        <div className="w-64 bg-slate-900 border-r border-slate-700 flex flex-col">

            {/* New Chat Button */}

            <button

                onClick={onNewChat}

                className="m-4 bg-blue-600 hover:bg-blue-700 rounded-lg p-3 flex items-center justify-center gap-2"

            >

                <FaPlus />

                New Chat

            </button>

            {/* Chat History */}

            <div className="px-4 mt-6">

                <h2 className="text-gray-400 mb-3 flex items-center gap-2">

                    <FaHistory />

                    Recent Chats

                </h2>

                {

                    chats.length === 0 ? (

                        <div className="text-sm text-gray-500">

                            No chats yet

                        </div>

                    ) : (

                        chats.map(chat => (

                            <div

                                key={chat.id}

                                className="flex items-center gap-2 mb-2"

                            >

                                {/* Open Chat */}

                                <button

                                    onClick={() => onSelectChat(chat)}

                                    className="flex-1 text-left bg-slate-800 hover:bg-slate-700 rounded-lg p-2"

                                >

                                    {chat.title}

                                </button>

                                {/* Delete Chat */}

                                <button

                                    onClick={() => onDeleteChat(chat.id)}

                                    className="text-red-400 hover:text-red-600 p-2"

                                >

                                    <FaTrash />

                                </button>

                            </div>

                        ))

                    )

                }

            </div>

        </div>

    );

}

export default Sidebar;