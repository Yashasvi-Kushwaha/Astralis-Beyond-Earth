import logo from "../assets/astralis-logo.png";

function Hero() {
    return (

        <section className="flex flex-col items-center justify-center text-center pt-20">

            <img
                src={logo}
                alt="Astralis"
                className="w-36 mb-6 animate-fade"
            />

            <h1
                className="
                text-7xl
                font-light
                tracking-[0.35em]
                text-white
                "
            >
                ASTRALIS
            </h1>

            <h2
                className="
                mt-4
                text-3xl
                tracking-[0.4em]
                text-violet-400
                font-light
                "
            >
                BEYOND EARTH
            </h2>

            <p
                className="
                mt-10
                max-w-3xl
                text-2xl
                text-slate-200
                leading-relaxed
                "
            >
                An AI-Powered Astronomy Learning and
                Research Assistant
            </p>

            <p
                className="
                mt-6
                text-xl
                text-slate-400
                "
            >
                Explore • Learn • Discover
            </p>

        </section>

    );
}

export default Hero;