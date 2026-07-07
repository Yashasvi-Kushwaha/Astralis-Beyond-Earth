import { FaRocket } from "react-icons/fa";
import { MdOutlineScience } from "react-icons/md";
import logo from "../assets/astralis-logo.png";

function Navbar() {
    return (
        <div className="w-full h-16 bg-slate-900 border-b border-slate-700 flex items-center px-6">

            <img
                src={logo}
                alt="Astralis"
                className="w-10 h-10 object-contain"
            />

            <div className="ml-3">

                <h1 className="text-2xl font-bold tracking-widest">
                    ASTRALIS
                </h1>

                <p className="text-sm text-violet-400">
                    Beyond Earth
                </p>

            </div>

        </div>
    );
}

export default Navbar;
