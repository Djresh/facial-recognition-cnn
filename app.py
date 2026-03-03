from flask import Flask, jsonify, request
from flask_cors import CORS
import numpy as np
import cv2
import base64
import os
import json
from recognize import load_recognition_model, recognize_faces_in_frame
from database import log_recognition, get_recent_logs, get_recognition_stats, create_tables

app = Flask(__name__)
CORS(app)

MODEL_PATH  = "model/cnn_face_model.h5"
LABELS_PATH = "model/class_labels.json"

# Ensure DB tables exist on startup
try:
    create_tables()
except Exception as db_err:
    print(f"DB warning: {db_err} - MySQL may not be configured yet.")

print("Loading CNN model...")
model, labels = (None, {})
if os.path.exists(MODEL_PATH) and os.path.exists(LABELS_PATH):
    model, labels = load_recognition_model()
    print(f"Model loaded. Classes: {list(labels.values())}")
else:
    print("Model not found. Train first with: python train.py")

@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "model_loaded": model is not None,
                    "num_classes": len(labels)})

@app.route("/api/recognize", methods=["POST"])
def recognize():
    if model is None:
        return jsonify({"error": "Model not loaded. Run train.py first."}), 503
    data = request.get_json()
    if not data or "image" not in data:
        return jsonify({"error": "No image provided."}), 400
    try:
        img_data = base64.b64decode(data["image"])
        nparr    = np.frombuffer(img_data, np.uint8)
        frame    = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if frame is None:
            return jsonify({"error": "Invalid image data."}), 400
        _, results = recognize_faces_in_frame(frame, model, labels)
        for r in results:
            log_recognition(r["name"], r["confidence"])
        return jsonify({"faces_detected": len(results), "results": results})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/logs", methods=["GET"])
def get_logs():
    limit = int(request.args.get("limit", 20))
    try:
        df = get_recent_logs(limit)
        df["recognized_at"] = df["recognized_at"].astype(str)
        return jsonify({"logs": df.to_dict(orient="records")})
    except Exception as e:
        return jsonify({"error": str(e), "logs": []}), 500

@app.route("/api/stats", methods=["GET"])
def get_stats():
    try:
        df = get_recognition_stats()
        df["last_seen"]       = df["last_seen"].astype(str)
        df["avg_confidence"]  = df["avg_confidence"].astype(float).round(4)
        return jsonify({"stats": df.to_dict(orient="records")})
    except Exception as e:
        return jsonify({"error": str(e), "stats": []}), 500

@app.route("/api/classes", methods=["GET"])
def get_classes():
    return jsonify({"classes": list(labels.values()), "total": len(labels)})

@app.route("/api/reload-model", methods=["POST"])
def reload_model():
    global model, labels
    if os.path.exists(MODEL_PATH) and os.path.exists(LABELS_PATH):
        model, labels = load_recognition_model()
        return jsonify({"status": "Model reloaded successfully",
                        "classes": list(labels.values())})
    return jsonify({"error": "Model files not found. Run train.py first."}), 404

if __name__ == "__main__":
    app.run(debug=True, port=5000)
