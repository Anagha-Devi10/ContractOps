import React, { useState } from "react";

export default function ContractUpload({ onUploaded }) {
  const [title, setTitle] = useState("");
  const [text, setText] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!title.trim() || !text.trim()) return;
    setLoading(true);
    try {
      await onUploaded(title.trim(), text.trim());
      setTitle("");
      setText("");
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} style={{ display: "flex", flexDirection: "column", gap: 10 }}>
      <div>
        <div className="input-label">Contract Title</div>
        <input
          className="input"
          placeholder="e.g. Service Agreement with Alpha Corp"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
        />
      </div>

      <div>
        <div className="input-label">Contract Text</div>
        <textarea
          className="input textarea"
          placeholder="Paste or type your contract text here..."
          value={text}
          onChange={(e) => setText(e.target.value)}
        />
      </div>

      <div style={{ display: "flex", justifyContent: "flex-end", gap: 8 }}>
        <button type="submit" className="btn" disabled={loading}>
          {loading ? "Processing..." : "Process Contract"}
        </button>
      </div>
    </form>
  );
}
