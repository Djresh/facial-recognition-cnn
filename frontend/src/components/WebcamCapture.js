import React, { useRef, useCallback, useState } from "react";
import Webcam from "react-webcam";

const WebcamCapture = ({ onCapture, isProcessing }) => {
  const webcamRef                   = useRef(null);
  const [webcamError, setWebcamError] = useState(null);

  const capture = useCallback(() => {
    const imageSrc = webcamRef.current?.getScreenshot();
    if (imageSrc) {
      const base64 = imageSrc.split(",")[1]; // remove data:image/jpeg;base64, prefix
      onCapture(base64, imageSrc);
    }
  }, [onCapture]);

  return (
    <div className="card shadow-sm p-3 mb-4">
      <h5 className="card-title text-primary">📷 Live Webcam Feed</h5>
      {webcamError ? (
        <div className="alert alert-warning">
          Webcam not available: {webcamError}. Please allow camera access.
        </div>
      ) : (
        <div className="text-center">
          <Webcam
            ref={webcamRef}
            screenshotFormat="image/jpeg"
            width={480}
            height={360}
            className="rounded border"
            onUserMediaError={(e) => setWebcamError(e.message || "Camera error")}
          />
        </div>
      )}
      <div className="text-center mt-3">
        <button
          className="btn btn-primary btn-lg px-5"
          onClick={capture}
          disabled={isProcessing || !!webcamError}
        >
          {isProcessing
            ? <><span className="spinner-border spinner-border-sm me-2" />Recognizing...</>
            : "📸 Capture & Recognize"}
        </button>
      </div>
    </div>
  );
};

export default WebcamCapture;
