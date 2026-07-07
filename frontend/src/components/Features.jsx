import {
    FaBookOpen,
    FaFileAlt,
    FaRobot,
    FaCompass,
    FaSatellite
} from "react-icons/fa";

const features = [

    {
        icon: <FaBookOpen size={42} />,
        title: "LEARN",
        text: "Simplified astronomy concepts."
    },

    {
        icon: <FaFileAlt size={42} />,
        title: "RESEARCH",
        text: "Understand research papers."
    },

    {
        icon: <FaSatellite size={42} />,
        title: "DISCOVER",
        text: "Latest missions & discoveries."
    },

    {
        icon: <FaCompass size={42} />,
        title: "GUIDE",
        text: "Personalized learning roadmap."
    },

    {
        icon: <FaRobot size={42} />,
        title: "AI Mode",
        text: "Ask anything related to space and cosmos."
    }

];

function Features() {

    return (

        <section className="mt-24 w-full max-w-7xl px-10">

            <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-5 gap-8">

                {

                    features.map((feature, index) => (

                        <div

                            key={index}

                            className="
                            bg-white/5
                            backdrop-blur-md
                            border
                            border-violet-500/20
                            rounded-3xl
                            p-8
                            text-center
                            transition-all
                            duration-300
                            hover:scale-105
                            hover:border-violet-400
                            hover:shadow-[0_0_35px_rgba(168,85,247,0.45)]
                            "

                        >

                            <div className="text-violet-400 flex justify-center mb-6">

                                {feature.icon}

                            </div>

                            <h2 className="text-lg font-semibold tracking-wider">

                                {feature.title}

                            </h2>

                            <p className="mt-4 text-slate-300 text-sm leading-6">

                                {feature.text}

                            </p>

                        </div>

                    ))

                }

            </div>

        </section>

    );

}

export default Features;