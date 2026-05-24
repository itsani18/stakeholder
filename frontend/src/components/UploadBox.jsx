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

      // FILE
      if (file) {

        formData.append(
          "file",
          file
        );
      }

      // TEXT COMMENTS
      if (comments.trim()) {

        const blob = new Blob(
          [comments],
          {
            type: "text/plain",
          }
        );

        formData.append(
          "file",
          blob,
          "comments.txt"
        );
      }

      // API CALL
      const analysisResponse = await axios.post(

        "http://127.0.0.1:5000/api/analyze-file",

        formData,

        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );

      const data = analysisResponse.data;
      console.log(data);
      // SENTIMENT COUNTS
      const positiveCount =
        data.sentiment.positive || 0;

      const negativeCount =
        data.sentiment.negative || 0;

      const neutralCount =
        data.sentiment.neutral || 0;

      const mixedCount =
        data.sentiment.mixed || 0;

      const total =
        positiveCount +
        negativeCount +
        neutralCount +
        mixedCount;

      // FORMAT DATA
      const formattedData = {

        summary: data.summary,

        keywords: data.words.map(
          (w) => w.word
        ),

        comments: data.items.map(
          (item) => item.comment
        ),

        wordcloud:
          data.wordcloud,

        sentiment: {

          positive:
            total > 0
              ? Math.round((positiveCount / total) * 100)
              : 0,

          negative:
            total > 0
              ? Math.round((negativeCount / total) * 100)
              : 0,

          neutral:
            total > 0
              ? Math.round((neutralCount / total) * 100)
              : 0,

          mixed:
            total > 0
              ? Math.round((mixedCount / total) * 100)
              : 0,
        },
      };

      // SAVE
      localStorage.setItem(

        "analysis",

        JSON.stringify(formattedData)
      );

      // NAVIGATE
      navigate("/dashboard", {

        state: {
          analysis: formattedData,
        },
      });

    } catch (error) {

      console.log(error);

      alert(
        "Analysis failed. Check backend terminal."
      );

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

          <Upload
            size={45}
            className="mx-auto text-cyan-400"
          />

          <input
            type="file"
            className="mt-5"
            onChange={(e) =>
              setFile(e.target.files[0])
            }
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
          onChange={(e) =>
            setComments(e.target.value)
          }
        />

      </div>

      <button
        onClick={handleAnalyze}
        className="w-full mt-8 bg-cyan-500 hover:bg-cyan-400 transition py-4 rounded-2xl text-lg font-bold"
      >
        {loading
          ? "Analyzing..."
          : "Analyze"}
      </button>

    </div>
  );
}

export default UploadBox;