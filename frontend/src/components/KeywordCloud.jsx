function KeywordCloud({ keywords }) {

  return (
    <div className="bg-slate-900 rounded-3xl p-8 border border-slate-800">

      <h2 className="text-3xl font-bold mb-8">
        Extracted Keywords
      </h2>

      <div className="flex flex-wrap gap-4">

        {keywords.map((word, index) => (
          <div
            key={index}
            className="px-5 py-3 rounded-2xl bg-cyan-500/10 border border-cyan-400/30 text-cyan-300 text-lg"
          >
            {word}
          </div>
        ))}
      </div>
    </div>
  );
}

export default KeywordCloud;