import React from "react";

const RecognitionHistory = ({ logs }) => {
  if (!logs || logs.length === 0)
    return <p className="text-muted">No recognition logs yet.</p>;

  return (
    <div className="card shadow-sm p-3 mb-4">
      <h5 className="card-title text-secondary">📋 Recognition History</h5>
      <div className="table-responsive">
        <table className="table table-sm table-striped table-hover">
          <thead className="table-dark">
            <tr>
              <th>Person</th>
              <th>Confidence</th>
              <th>Time</th>
              <th>Source</th>
            </tr>
          </thead>
          <tbody>
            {logs.map((log, i) => (
              <tr key={i}>
                <td className="fw-bold">{log.person_name}</td>
                <td>
                  <span className={"badge " + (
                    log.confidence >= 0.85 ? "bg-success" :
                    log.confidence >= 0.70 ? "bg-warning text-dark" : "bg-danger"
                  )}>
                    {(log.confidence * 100).toFixed(1)}%
                  </span>
                </td>
                <td style={{ fontSize: "0.8rem" }}>{log.recognized_at}</td>
                <td><span className="badge bg-secondary">{log.image_source}</span></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default RecognitionHistory;
