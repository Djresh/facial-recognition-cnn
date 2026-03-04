import React from "react";

const ConfidenceBar = ({ value }) => {
  const pct   = Math.round(value * 100);
  const color = pct >= 85 ? "bg-success" : pct >= 70 ? "bg-warning" : "bg-danger";
  return (
    <div className="progress mt-1" style={{ height: "10px" }}>
      <div className={"progress-bar " + color} style={{ width: pct + "%" }} />
    </div>
  );
};

const RecognitionResult = ({ snapshot, results }) => {
  if (!results) return null;
  return (
    <div className="card shadow-sm p-3 mb-4">
      <h5 className="card-title text-success">🔍 Recognition Result</h5>
      <div className="row">
        {snapshot && (
          <div className="col-md-5 text-center mb-3">
            <img src={snapshot} alt="Captured"
              className="img-fluid rounded border" style={{ maxHeight: "240px" }} />
            <p className="text-muted mt-1" style={{ fontSize: "0.8rem" }}>Captured frame</p>
          </div>
        )}
        <div className="col-md-7">
          {results.length === 0 ? (
            <div className="alert alert-info">
              No faces detected. Try better lighting or move closer.
            </div>
          ) : results.map((r, i) => (
            <div key={i} className="border rounded p-3 mb-2 bg-light">
              <div className="d-flex justify-content-between">
                <span className="fw-bold fs-5">
                  {r.name === "Unknown" ? "❓ Unknown Person" : "✅ " + r.name}
                </span>
                <span className={"badge " + (r.name === "Unknown" ? "bg-danger" : "bg-success")}>
                  {r.name === "Unknown" ? "Not Recognized" : "Recognized"}
                </span>
              </div>
              <small className="text-muted">
                Confidence: <strong>{(r.confidence * 100).toFixed(1)}%</strong>
              </small>
              <ConfidenceBar value={r.confidence} />
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default RecognitionResult;
