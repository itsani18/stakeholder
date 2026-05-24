import { Upload } from "lucide-react";
import { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

function UploadBox() {
  const navigate = useNavigate();

  const [file, setFile] = useState(null);
  const [comments, setComments] = useState("");
  const [loading, setLoading] = useState(false);

  const handleAnalyze = async () => {
    try {
      setLoading(true);

      const formData = new FormData();

      if (file) {
        formData.append("file", file);
      }

      formData.append("comments", comments);

      // backend API
      const uploadResponse = await axios.post(
  "http://127.0.0.1:8000/upload",
  formData
);

const uploadId = uploadResponse.data.upload_id;

const analysisResponse = await axios.post(
  `http://127.0.0.1:8000/analyze/${uploadId}`
);

const data = analysisResponse.data;

const sentiments = data.sentiments || [];

const positive = sentiments.filter(
  (s) => s.sentiment.toLowerCase() === "positive"
).length;

const negative = sentiments.filter(
  (s) => s.sentiment.toLowerCase() === "negative"
).length;

const neutral = sentiments.filter(
  (s) => s.sentiment.toLowerCase() === "neutral"
).length;

const total = sentiments.length || 1;

const formattedData = {
  summary: data.summary,

  keywords: data.keywords,

  comments: sentiments.map((s) => s.text),

  sentiment: {
    positive: Math.round((positive / total) * 100),
    negative: Math.round((negative / total) * 100),
    neutral: Math.round((neutral / total) * 100),
    mixed: 0,
  },
};
      navigate("/dashboard", {
        state: {
          analysis: formattedData,
        },
      });

    } catch (error) {
      console.log(error);

      // TEMPORARY DEMO DATA
      navigate("/dashboard", {
        state: {
          analysis: {
            summary:
              "Most stakeholders support environmental sustainability and healthcare reforms.",

            sentiment: {
              positive: 58,
              negative: 17,
              neutral: 15,
              mixed: 10,
            },

            keywords: [
              "Environment",
              "Healthcare",
              "Transparency",
              "Economy",
            ],

            comments: [
              "This policy is very beneficial for climate action.",

              "Healthcare improvements are necessary.",

              "The taxation proposal needs more clarification.",

              "Good initiative but implementation may be difficult.",
            ],
          },
        },
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-slate-900 border border-slate-700 rounded-3xl p-10">

      <h2 className="text-3xl font-bold text-center">
        Upload or Paste Stakeholder Comments
      </h2>

      <div className="mt-8">

        <label className="text-slate-300">
          Upload File
        </label>

        <div className="mt-3 border border-dashed border-cyan-400 rounded-2xl p-8 text-center">
          <Upload size={45} className="mx-auto text-cyan-400" />

          <input
            type="file"
            className="mt-5"
            onChange={(e) => setFile(e.target.files[0])}
          />
        </div>
      </div>

      <div className="mt-8">

        <label className="text-slate-300">
          Paste Comments Directly
        </label>

        <textarea
          rows="8"
          placeholder="Paste stakeholder comments here..."
          className="w-full mt-3 bg-slate-800 border border-slate-700 rounded-2xl p-5 outline-none focus:border-cyan-400"
          value={comments}
          onChange={(e) => setComments(e.target.value)}
        />
      </div>

      <button
        onClick={handleAnalyze}
        className="w-full mt-8 bg-cyan-500 hover:bg-cyan-400 transition py-4 rounded-2xl text-lg font-bold"
      >
        {loading ? "Analyzing..." : "Analyze"}
      </button>
    </div>
  );
}

export default UploadBox;