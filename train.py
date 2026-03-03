import os, json
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout, BatchNormalization
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau
from tensorflow.keras.optimizers import Adam
from preprocess import get_data_generators

IMG_SIZE    = 64
BATCH_SIZE  = 32
EPOCHS      = 50
DATASET_DIR = "dataset"
MODEL_PATH  = "model/cnn_face_model.h5"
LABELS_PATH = "model/class_labels.json"

def build_cnn(num_classes):
    model = Sequential([
        Conv2D(32, (3,3), activation='relu', padding='same', input_shape=(IMG_SIZE, IMG_SIZE, 3)),
        BatchNormalization(), MaxPooling2D(2, 2),
        Conv2D(64, (3,3), activation='relu', padding='same'),
        BatchNormalization(), MaxPooling2D(2, 2),
        Conv2D(128, (3,3), activation='relu', padding='same'),
        BatchNormalization(), MaxPooling2D(2, 2),
        Flatten(),
        Dense(512, activation='relu'),
        Dropout(0.5),
        Dense(num_classes, activation='softmax')
    ])
    model.compile(optimizer=Adam(learning_rate=0.001),
                  loss='categorical_crossentropy', metrics=['accuracy'])
    model.summary()
    return model

def train():
    os.makedirs("model", exist_ok=True)
    if not os.path.exists(DATASET_DIR):
        print("Dataset folder not found.")
        print("Create: dataset/person_name/image.jpg")
        return
    train_gen, val_gen = get_data_generators(DATASET_DIR, BATCH_SIZE)
    num_classes = len(train_gen.class_indices)
    print(f"Classes found: {num_classes} -> {train_gen.class_indices}")
    with open(LABELS_PATH, 'w') as f:
        json.dump({v: k for k, v in train_gen.class_indices.items()}, f)
    model = build_cnn(num_classes)
    callbacks = [
        EarlyStopping(monitor='val_accuracy', patience=8, restore_best_weights=True),
        ModelCheckpoint(MODEL_PATH, save_best_only=True, monitor='val_accuracy'),
        ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=4, min_lr=1e-6)
    ]
    history = model.fit(train_gen, epochs=EPOCHS,
                        validation_data=val_gen, callbacks=callbacks)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    ax1.plot(history.history['accuracy'], label='Train')
    ax1.plot(history.history['val_accuracy'], label='Val')
    ax1.set_title('Accuracy'); ax1.legend()
    ax2.plot(history.history['loss'], label='Train')
    ax2.plot(history.history['val_loss'], label='Val')
    ax2.set_title('Loss'); ax2.legend()
    plt.savefig("model/training_history.png")
    plt.close()
    print(f"Model saved: {MODEL_PATH}")
    print(f"Labels saved: {LABELS_PATH}")

if __name__ == "__main__":
    train()
