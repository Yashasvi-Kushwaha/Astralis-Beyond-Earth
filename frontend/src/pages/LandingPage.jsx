import { useNavigate } from "react-router-dom";

import bg from "../assets/space-bg.jpg";

import Hero from "../components/Hero";
import Features from "../components/Features";
import Topics from "../components/Topics";

function LandingPage() {

    const navigate = useNavigate();

    return (

        <div
            className="min-h-screen w-screen bg-cover bg-center text-white relative overflow-hidden"
            style={{
                backgroundImage: `url(${bg})`
            }}
        >

            {/* Dark Overlay */}

            <div className="absolute inset-0 bg-black/50"></div>

            {/* Content */}

            <div className="relative z-10 flex flex-col items-center">

                <Hero />

                <Features />

                <Topics />

                <button
                    onClick={() => navigate("/chat")}
                    className="
                        mt-12
                        mb-20
                        px-10
                        py-4
                        rounded-full
                        border
                        border-violet-500
                        bg-black/30
                        hover:bg-violet-700
                        transition
                        duration-300
                        text-lg
                    "
                >
                    Start Exploring →
                </button>

            </div>

        </div>

    );

}

export default LandingPage;