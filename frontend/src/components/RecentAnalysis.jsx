import { FileText } from "lucide-react";

const analyses = [
  {
    title: "Environmental Policy Draft",
    date: "2 hours ago",
    sentiment: "Positive",
  },
  {
    title: "Healthcare Reform Bill",
    date: "5 hours ago",
    sentiment: "Neutral",
  },
  {
    title: "Data Privacy Regulation",
    date: "1 day ago",
    sentiment: "Negative",
  },
];

function RecentAnalysis() {
  return (
    <div className="bg-slate-900 rounded-3xl p-8 border border-slate-800 mt-10">
      <h2 className="text-2xl font-bold mb-8">
        Recent Analyses
      </h2>

      <div className="space-y-5">
        {analyses.map((item, index) => (
          <div
            key={index}
            className="flex items-center justify-between bg-slate-800 p-5 rounded-2xl"
          >
            <div className="flex items-center gap-4">
              <FileText className="text-cyan-400" />

              <div>
                <h3 className="font-semibold text-lg">
                  {item.title}
                </h3>

                <p className="text-slate-400 text-sm">
                  {item.date}
                </p>
              </div>
            </div>

            <div
              className={`px-4 py-2 rounded-xl text-sm font-semibold
                ${
                  item.sentiment === "Positive"
                    ? "bg-green-500/20 text-green-400"
                    : item.sentiment === "Negative"
                    ? "bg-red-500/20 text-red-400"
                    : "bg-yellow-500/20 text-yellow-300"
                }`}
            >
              {item.sentiment}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default RecentAnalysis;