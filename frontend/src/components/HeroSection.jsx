import { motion } from "framer-motion";

function HeroSection() {
  return (
    <section className="min-h-[85vh] flex flex-col justify-center items-center text-center px-6">
      <motion.h1
        initial={{ opacity: 0, y: -30 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-6xl font-bold leading-tight"
      >
        AI-Powered Stakeholder
        <span className="text-cyan-400"> Feedback Analyzer</span>
      </motion.h1>

      <p className="mt-6 text-slate-400 max-w-3xl text-lg">
        Analyze stakeholder comments on draft legislation using
        sentiment detection, AI summarization, and keyword insights.
      </p>

      <button className="mt-10 px-8 py-4 rounded-2xl bg-cyan-500 hover:bg-cyan-400 transition text-lg font-semibold">
        Start Analysis
      </button>
    </section>
  );
}

export default HeroSection;