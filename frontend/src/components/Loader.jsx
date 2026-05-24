function Loader() {
  return (
    <div className="flex flex-col items-center justify-center py-20">
      <div className="w-16 h-16 border-4 border-cyan-400 border-t-transparent rounded-full animate-spin"></div>

      <p className="mt-6 text-slate-400 text-lg">
        AI is analyzing stakeholder comments...
      </p>
    </div>
  );
}

export default Loader;