import {
  PieChart,
  Pie,
  Tooltip,
  ResponsiveContainer,
  Cell,
  Legend,
} from "recharts";

function SentimentChart({ sentiment }) {

  const data = [
    {
      name: "Positive",
      value: sentiment.positive,
    },
    {
      name: "Negative",
      value: sentiment.negative,
    },
    {
      name: "Neutral",
      value: sentiment.neutral,
    },
    {
      name: "Mixed",
      value: sentiment.mixed,
    },
  ];

  const COLORS = [
    "#22c55e",
    "#ef4444",
    "#eab308",
    "#06b6d4",
  ];

  return (
    <div className="bg-slate-900 rounded-3xl p-8 border border-slate-800 h-[450px]">

      <h2 className="text-3xl font-bold mb-8">
        Sentiment Analysis
      </h2>

      <ResponsiveContainer width="100%" height="100%">

        <PieChart>

          <Pie
            data={data}
            dataKey="value"
            outerRadius={130}
            label
          >
            {data.map((entry, index) => (
              <Cell
                key={index}
                fill={COLORS[index]}
              />
            ))}
          </Pie>

          <Tooltip />

          <Legend />

        </PieChart>

      </ResponsiveContainer>
    </div>
  );
}

export default SentimentChart;