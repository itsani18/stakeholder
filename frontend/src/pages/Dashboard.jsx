import { useLocation } from "react-router-dom";

import Navbar from "../components/Navbar";
import StatsCards from "../components/StatsCards";
import SentimentChart from "../components/SentimentChart";
import KeywordCloud from "../components/KeywordCloud";
import Footer from "../components/Footer";

function Dashboard() {

  const location = useLocation();

  const analysis = location.state?.analysis;

  if (!analysis) {
    return (
      <div className="text-white text-center mt-20">
        No analysis data found.
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-950 text-white">

      <Navbar />

      <div className="max-w-7xl mx-auto px-6 py-10">

        <h1 className="text-5xl font-bold">
          AI Analysis Dashboard
        </h1>

        <p className="mt-4 text-slate-400 text-lg">
          Real-time stakeholder sentiment and policy insights
        </p>

        <StatsCards sentiment={analysis.sentiment} />

        <div className="grid lg:grid-cols-2 gap-10 mt-10">

          <SentimentChart sentiment={analysis.sentiments} />

          <KeywordCloud keywords={analysis.keywords} />
        </div>

        <div className="bg-slate-900 rounded-3xl p-8 mt-10 border border-slate-800">

          <h2 className="text-3xl font-bold">
            AI Generated Summary
          </h2>

          <p className="mt-5 text-slate-300 leading-8 text-lg">
            {analysis.summary}
          </p>
        </div>

        <div className="bg-slate-900 rounded-3xl p-8 mt-10 border border-slate-800">

          <h2 className="text-3xl font-bold mb-8">
            Sample Stakeholder Comments
          </h2>

          <div className="space-y-5">

            {analysis.comments.map((comment, index) => (
              <div
                key={index}
                className="bg-slate-800 p-5 rounded-2xl text-slate-300"
              >
                {comment}
              </div>
            ))}
          </div>
        </div>

        <Footer />
      </div>
    </div>
  );
}

export default Dashboard;