import os
import cv2
import numpy as np
from tensorflow.keras.models import load_model


IMG_SIZE = 128

CLASS_NAMES = [
    "forged",
    "genuine"
]


class SignaturePredictor:

    def __init__(self, model_path):
        self.model = load_model(model_path)

    def preprocess(self, image_path):

        image = cv2.imread(
            image_path,
            cv2.IMREAD_GRAYSCALE
        )

        if image is None:
            raise ValueError(
                "Invalid or unreadable image."
            )

        image = cv2.resize(
            image,
            (IMG_SIZE, IMG_SIZE)
        )

        image = image.astype(
            np.float32
        ) / 255.0

        image = image.reshape(
            1,
            IMG_SIZE,
            IMG_SIZE,
            1
        )

        return image

    def predict(self, image_path):

        image = self.preprocess(
            image_path
        )

        prediction = self.model.predict(
            image,
            verbose=0
        )[0]

        index = int(
            np.argmax(prediction)
        )

        label = CLASS_NAMES[index]

        confidence = float(
            prediction[index] * 100
        )

        forged_probability = float(
            prediction[0] * 100
        )

        genuine_probability = float(
            prediction[1] * 100
        )

        return {
            "label": label.capitalize(),
            "confidence": round(
                confidence,
                2
            ),
            "forged_probability": round(
                forged_probability,
                2
            ),
            "genuine_probability": round(
                genuine_probability,
                2
            )
        }