import Navbar from "../components/Navbar";

function Results() {
  return (
    <div className="min-h-screen">
      <Navbar />

      <div className="max-w-5xl mx-auto py-20 px-6">
        <div className="bg-slate-900 rounded-3xl p-10">
          <h1 className="text-4xl font-bold">
            AI Generated Summary
          </h1>

          <p className="mt-6 text-slate-300 leading-8">
            The majority of stakeholders support the proposed
            legislation, especially regarding environmental
            sustainability and transparency measures.
          </p>
        </div>
      </div>
    </div>
  );
}

export default Results;