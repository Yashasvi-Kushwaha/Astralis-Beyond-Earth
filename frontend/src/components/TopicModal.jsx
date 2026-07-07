function TopicModal({ topic, onClose, onAsk }) {

    if (!topic) return null;

    return (
        <div className="fixed inset-0 bg-black/70 flex items-center justify-center z-50">

            <div className="bg-slate-900 rounded-2xl p-8 w-[520px] border border-cyan-500">

                <h1 className="text-3xl font-bold text-cyan-400">
                    {topic.title}
                </h1>

                <p className="mt-5 text-slate-300 leading-7">
                    {topic.definition}
                </p>

                <div className="mt-6 bg-slate-800 p-4 rounded-xl border-l-4 border-yellow-400">
                    <h3 className="font-bold mb-2">
                        🌟 Did You Know?
                    </h3>

                    <p>{topic.fact}</p>
                </div>

                <div className="flex justify-end gap-4 mt-8">

                    <button
                        onClick={onClose}
                        className="px-5 py-2 rounded-lg bg-slate-700 hover:bg-slate-600"
                    >
                        Close
                    </button>

                    <button
                        onClick={() => onAsk(topic.title)}
                        className="px-5 py-2 rounded-lg bg-cyan-600 hover:bg-cyan-700"
                    >
                        Ask Astralis →
                    </button>

                </div>

            </div>

        </div>
    );
}

export default TopicModal;