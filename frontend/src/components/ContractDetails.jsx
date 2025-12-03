import React from "react";

export default function ContractDetails({ contract }) {
  return (
    <div className="contract-details">
      <div className="details-header">
        <div>
          <h2 style={{ fontSize: "1.05rem", fontWeight: 600 }}>
            {contract.title}
          </h2>
          <div className="helper-text">Contract ID: {contract.contract_id}</div>
        </div>
        <span className="badge-soft">
          Confidence {contract.confidence.toFixed(2)}
        </span>
      </div>

      <div className="details-grid">
        <div>
          <div className="details-field-label">Parties</div>
          <div className="details-field-value">
            {contract.parties || "Not detected"}
          </div>
        </div>
        <div>
          <div className="details-field-label">Effective Date</div>
          <div className="details-field-value">
            {contract.effective_date || "N/A"}
          </div>
        </div>
        <div>
          <div className="details-field-label">Expiry Date</div>
          <div className="details-field-value">
            {contract.expiry_date || "N/A"}
          </div>
        </div>
        <div>
          <div className="details-field-label">Payment Terms</div>
          <div className="details-field-value">
            {contract.payment_terms || "Not specified"}
          </div>
        </div>
      </div>

      {contract.renewal_terms && (
        <div className="summary-box">
          <span className="details-field-label">Renewal Terms</span>
          <div className="details-field-value">{contract.renewal_terms}</div>
        </div>
      )}

      {contract.summary && (
        <div className="summary-box">
          <span className="details-field-label">Summary</span>
          <div>{contract.summary}</div>
        </div>
      )}

      <div className="summary-box">
        <span className="details-field-label">Obligations</span>
        <div className="obligations-list">
          {contract.obligations && contract.obligations.length > 0 ? (
            contract.obligations.map((o, idx) => (
              <div key={idx} className="obligation-item">
                {o.obligation}{" "}
                <span style={{ color: "#9ca3af", fontSize: "0.75rem" }}>
                  (conf {o.confidence})
                </span>
              </div>
            ))
          ) : (
            <span className="helper-text">No obligations detected.</span>
          )}
        </div>
      </div>
    </div>
  );
}
