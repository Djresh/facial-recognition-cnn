import cv2
import numpy as np
import json
from tensorflow.keras.models import load_model
from preprocess import preprocess_frame

MODEL_PATH           = "model/cnn_face_model.h5"
LABELS_PATH          = "model/class_labels.json"
IMG_SIZE             = 64
CONFIDENCE_THRESHOLD = 0.70

def load_recognition_model():
    model = load_model(MODEL_PATH)
    with open(LABELS_PATH, 'r') as f:
        labels = json.load(f)
    return model, labels

def recognize_faces_in_frame(frame, model, labels):
    face_data = preprocess_frame(frame)
    results   = []
    for fd in face_data:
        face_array   = fd["face_array"]
        x, y, w, h   = fd["bbox"]
        input_tensor = np.expand_dims(face_array, axis=0)
        predictions  = model.predict(input_tensor, verbose=0)[0]
        confidence   = float(np.max(predictions))
        class_idx    = int(np.argmax(predictions))
        name  = labels.get(str(class_idx), "Unknown") if confidence >= CONFIDENCE_THRESHOLD else "Unknown"
        color = (0, 255, 0) if name != "Unknown" else (0, 0, 255)
        cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
        cv2.putText(frame, f"{name} ({confidence*100:.1f}%)",
                    (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
        results.append({"name": name, "confidence": round(confidence, 4),
                        "bbox": [x, y, w, h]})
    return frame, results

def run_webcam_demo():
    model, labels = load_recognition_model()
    cap = cv2.VideoCapture(0)
    print("Press 'q' to quit.")
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        annotated_frame, results = recognize_faces_in_frame(frame, model, labels)
        for r in results:
            print(f"Detected: {r['name']} | Confidence: {r['confidence']*100:.1f}%")
        cv2.imshow("Facial Recognition", annotated_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    run_webcam_demo()
