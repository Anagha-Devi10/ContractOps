import React, { useState } from "react";
import axios from "axios";

export default function QaPanel({ contract, apiBase }) {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);

  const handleAsk = async (e) => {
    e.preventDefault();
    if (!question.trim()) return;
    setLoading(true);
    try {
      const res = await axios.post(
        `${apiBase}/contracts/${contract.contract_id}/qa`,
        { question: question.trim() }
      );
      setAnswer(res.data.answer);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="qa-container">
      <div className="panel-header" style={{ marginBottom: 2 }}>
        <h3 className="panel-title">Ask a Question</h3>
      </div>
      <p className="helper-text">
        Try: “When does this contract expire?”, “Who are the parties?”, or
        “What are the payment terms?”
      </p>

      <form onSubmit={handleAsk} className="qa-input-row">
        <input
          className="input"
          placeholder="Type your question about this contract..."
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
        />
        <button type="submit" className="btn btn-secondary" disabled={loading}>
          {loading ? "Thinking..." : "Ask"}
        </button>
      </form>

      {answer && (
        <div>
          <div className="qa-answer-label">Answer</div>
          <div className="qa-answer-text">{answer}</div>
        </div>
      )}
    </div>
  );
}
