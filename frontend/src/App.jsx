import React, { useEffect, useState } from "react";
import axios from "axios";
import ContractUpload from "./components/ContractUpload";
import ContractDetails from "./components/ContractDetails";
import QaPanel from "./components/QaPanel";

const API_BASE = "http://127.0.0.1:8000";

export default function App() {
  const [contracts, setContracts] = useState([]);
  const [selected, setSelected] = useState(null);

  const loadContracts = async () => {
    const res = await axios.get(`${API_BASE}/contracts`);
    setContracts(res.data);
    if (res.data.length > 0 && !selected) {
      setSelected(res.data[0]);
    }
  };

  useEffect(() => {
    loadContracts();
  }, []);

  const handleUploaded = async (title, text) => {
    await axios.post(`${API_BASE}/contracts`, { title, text });
    await loadContracts();
  };

  const handleSelect = (c) => setSelected(c);

  return (
    <div className="app-shell">
      {/* Header */}
      <header className="app-header">
        <div className="app-title-block">
          <div className="app-title">
            ContractOps
            <span className="app-title-badge">Enterprise Agent</span>
          </div>
          <p className="app-subtitle">
            AI-powered contract lifecycle assistant — extract key fields, track
            renewals, and ask questions in natural language.
          </p>
        </div>
        <div className="app-pills">
          <span className="app-pill">Multi-agent pipeline</span>
          <span className="app-pill">Extraction · Summary · QA</span>
          <span className="app-pill">FastAPI · React</span>
        </div>
      </header>

      {/* Body layout */}
      <div className="app-body">
        {/* Left: upload + contract list */}
        <section className="panel">
          <div className="panel-header">
            <h2 className="panel-title">Upload & Contracts</h2>
          </div>
          <ContractUpload onUploaded={handleUploaded} />

          <div style={{ marginTop: 14, display: "flex", justifyContent: "space-between", alignItems: "center" }}>
            <span className="helper-text">
              {contracts.length
                ? `Saved contracts: ${contracts.length}`
                : "No contracts yet. Upload your first contract to begin."}
            </span>
          </div>

          <div className="contract-list">
            {contracts.map((c) => (
              <button
                key={c.contract_id}
                className={
                  "contract-item" +
                  (selected && selected.contract_id === c.contract_id
                    ? " selected"
                    : "")
                }
                onClick={() => handleSelect(c)}
              >
                <span className="contract-item-title">{c.title}</span>
                <span className="contract-item-meta">
                  ID: {c.contract_id} · Confidence: {c.confidence.toFixed(2)}
                </span>
              </button>
            ))}
          </div>
        </section>

        {/* Right: details + QA */}
        <section className="panel">
          {selected ? (
            <>
              <ContractDetails contract={selected} />
              <QaPanel contract={selected} apiBase={API_BASE} />
            </>
          ) : (
            <p className="helper-text">
              Select or upload a contract to see extracted information and ask
              questions.
            </p>
          )}
        </section>
      </div>
    </div>
  );
}
