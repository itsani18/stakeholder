function StatsCards({ sentiment }) {

  const stats = [
    {
      title: "Positive",
      value: `${sentiment.positive}%`,
    },
    {
      title: "Negative",
      value: `${sentiment.negative}%`,
    },
    {
      title: "Neutral",
      value: `${sentiment.neutral}%`,
    },
    {
      title: "Mixed",
      value: `${sentiment.mixed}%`,
    },
  ];

  return (
    <div className="grid md:grid-cols-4 gap-6 mt-10">

      {stats.map((item, index) => (
        <div
          key={index}
          className="bg-slate-900 p-8 rounded-3xl border border-slate-800"
        >
          <h3 className="text-slate-400 text-lg">
            {item.title}
          </h3>

          <p className="text-5xl font-bold mt-4">
            {item.value}
          </p>
        </div>
      ))}
    </div>
  );
}

export default StatsCards;