import { Link } from "react-router-dom";
import { Scale } from "lucide-react";

function Navbar() {
  return (
    <nav className="flex justify-between items-center px-10 py-5 border-b border-slate-800 bg-slate-950">

      {/* LOGO */}

      <div className="flex items-center gap-2">

        <Scale className="text-cyan-400" />

        <h1 className="text-2xl font-bold text-white">
          Civic<span className="text-cyan-400">
            Lens AI
          </span>
        </h1>
      </div>

      {/* NAV LINKS */}

      <div className="flex gap-8 text-lg">

        <Link
          to="/"
          className="text-white hover:text-cyan-400 transition"
        >
          Home
        </Link>

        <Link
          to="/dashboard"
          className="text-white hover:text-cyan-400 transition"
        >
          Dashboard
        </Link>

        <Link
          to="/results"
          className="text-white hover:text-cyan-400 transition"
        >
          Analysis
        </Link>

      </div>
    </nav>
  );
}

export default Navbar;