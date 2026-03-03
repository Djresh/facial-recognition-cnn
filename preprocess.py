import cv2
import numpy as np
from tensorflow.keras.preprocessing.image import ImageDataGenerator

IMG_SIZE = 64

def load_and_preprocess_image(image_path):
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Cannot read image: {image_path}")
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    )
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1,
                                          minNeighbors=5, minSize=(30, 30))
    if len(faces) == 0:
        face_img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
    else:
        x, y, w, h = faces[0]
        face_img = img[y:y+h, x:x+w]
        face_img = cv2.resize(face_img, (IMG_SIZE, IMG_SIZE))
    face_img = face_img.astype("float32") / 255.0
    return face_img

def preprocess_frame(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    )
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1,
                                          minNeighbors=5, minSize=(30, 30))
    results = []
    for (x, y, w, h) in faces:
        face_crop    = frame[y:y+h, x:x+w]
        face_resized = cv2.resize(face_crop, (IMG_SIZE, IMG_SIZE))
        face_norm    = face_resized.astype("float32") / 255.0
        results.append({"face_array": face_norm, "bbox": (x, y, w, h)})
    return results

def get_data_generators(dataset_path, batch_size=32):
    train_datagen = ImageDataGenerator(
        rescale=1.0/255,
        rotation_range=20,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.15,
        zoom_range=0.15,
        horizontal_flip=True,
        brightness_range=[0.7, 1.3],
        validation_split=0.2
    )
    train_gen = train_datagen.flow_from_directory(
        dataset_path, target_size=(IMG_SIZE, IMG_SIZE),
        batch_size=batch_size, class_mode='categorical', subset='training'
    )
    val_gen = train_datagen.flow_from_directory(
        dataset_path, target_size=(IMG_SIZE, IMG_SIZE),
        batch_size=batch_size, class_mode='categorical', subset='validation'
    )
    return train_gen, val_gen
