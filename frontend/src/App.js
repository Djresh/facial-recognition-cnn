import React, { useState, useCallback, useEffect } from "react";
import WebcamCapture from "./components/WebcamCapture";
import RecognitionResult from "./components/RecognitionResult";
import RecognitionHistory from "./components/RecognitionHistory";
import { recognizeFace, fetchLogs, checkHealth } from "./services/api";

function App() {
  const [results, setResults]           = useState(null);
  const [snapshot, setSnapshot]         = useState(null);
  const [logs, setLogs]                 = useState([]);
  const [isProcessing, setIsProcessing] = useState(false);
  const [error, setError]               = useState(null);
  const [modelReady, setModelReady]     = useState(null);
  const [activeTab, setActiveTab]       = useState("webcam");

  useEffect(() => {
    checkHealth()
      .then(r => setModelReady(r.data.model_loaded))
      .catch(() => setModelReady(false));
    loadLogs();
  }, []);

  const loadLogs = async () => {
    try {
      const r = await fetchLogs(20);
      setLogs(r.data.logs || []);
    } catch {
      setLogs([]);
    }
  };

  const handleCapture = useCallback(async (base64, imageSrc) => {
    setIsProcessing(true);
    setError(null);
    setSnapshot(imageSrc);
    try {
      const res = await recognizeFace(base64);
      setResults(res.data.results);
      await loadLogs();
    } catch (e) {
      setError(e.response?.data?.error || "Recognition failed. Ensure Flask backend is running.");
      setResults([]);
    } finally {
      setIsProcessing(false);
    }
  }, []);

  return (
    <div className="container py-4">
      <div className="text-center mb-4">
        <h1 className="display-5 fw-bold text-primary">Facial Feature Recognition System</h1>
        <p className="text-muted">CNN Deep Learning — Python + OpenCV + React.js</p>
        {modelReady !== null && (
          <span className={"badge fs-6 " + (modelReady ? "bg-success" : "bg-warning text-dark")}>
            {modelReady ? "✅ Model Ready" : "⚠️ Model Not Loaded — Run train.py first"}
          </span>
        )}
      </div>

      <ul className="nav nav-tabs mb-4">
        <li className="nav-item">
          <button className={"nav-link " + (activeTab === "webcam" ? "active" : "")}
            onClick={() => setActiveTab("webcam")}>📷 Live Recognition</button>
        </li>
        <li className="nav-item">
          <button className={"nav-link " + (activeTab === "history" ? "active" : "")}
            onClick={() => setActiveTab("history")}>📋 History</button>
        </li>
      </ul>

      {error && <div className="alert alert-danger">{error}</div>}

      {activeTab === "webcam" && (
        <>
          <WebcamCapture onCapture={handleCapture} isProcessing={isProcessing} />
          <RecognitionResult snapshot={snapshot} results={results} />
        </>
      )}

      {activeTab === "history" && (
        <>
          <button className="btn btn-outline-secondary btn-sm mb-3" onClick={loadLogs}>
            🔄 Refresh Logs
          </button>
          <RecognitionHistory logs={logs} />
        </>
      )}

      <footer className="text-center text-muted mt-5 py-3 border-top">
        <small>Built by Reshma D J | CNN + OpenCV + React.js | M.E. Computer Science</small>
      </footer>
    </div>
  );
}

export default App;
