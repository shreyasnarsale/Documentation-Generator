import { useState } from "react";

const API_URL = "http://localhost:8000/api/random-quote";

function QuoteGenerator() {
  const [quote, setQuote] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const fetchQuote = async () => {
    setLoading(true);
    setError("");

    try {
      const response = await fetch(API_URL);

      if (!response.ok) {
        throw new Error("Failed to fetch quote");
      }

      const data = await response.json();
      setQuote(data.data.quote);
    } catch (err) {
      setError(
        "Error fetching quote. Make sure the backend server is running."
      );
      setQuote("");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-2xl w-full text-center">
      <h1 className="text-4xl font-bold mb-2 text-indigo-600 dark:text-indigo-400">
        Random Quote Generator
      </h1>
      <p className="text-gray-600 dark:text-gray-400 mb-8">
        Click the button to generate an inspirational quote
      </p>

      <button
        onClick={fetchQuote}
        disabled={loading}
        className="bg-indigo-600 hover:bg-indigo-700 disabled:bg-indigo-400 disabled:cursor-not-allowed text-white font-semibold py-3 px-6 rounded-lg transition-all duration-200 transform hover:-translate-y-0.5 active:translate-y-0 disabled:transform-none"
      >
        {loading ? "Generating..." : "Generate Quote"}
      </button>

      {error && (
        <div className="mt-6 p-4 bg-red-500 text-white rounded-lg text-sm">
          {error}
        </div>
      )}

      {quote && (
        <div className="mt-8 p-8 bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 shadow-lg">
          <p className="text-xl leading-relaxed text-gray-800 dark:text-gray-200 italic">
            {quote}
          </p>
        </div>
      )}
    </div>
  );
}

export default QuoteGenerator;
