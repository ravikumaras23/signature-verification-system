import cv2
import numpy as np
from tensorflow.keras.models import load_model


IMG_SIZE = 128


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
        )

        # Binary sigmoid model:
        # output is a single probability.
        #
        # 0 = Forged
        # 1 = Genuine
        genuine_probability = float(
            prediction[0][0]
        )

        forged_probability = (
            1.0 - genuine_probability
        )

        # Convert probabilities to percentages
        genuine_percentage = (
            genuine_probability * 100
        )

        forged_percentage = (
            forged_probability * 100
        )

        # Binary classification threshold
        if genuine_probability >= 0.5:
            label = "Genuine"
            confidence = genuine_percentage
        else:
            label = "Forged"
            confidence = forged_percentage

        return {
            "label": label,
            "confidence": round(
                confidence,
                2
            ),
            "forged_probability": round(
                forged_percentage,
                2
            ),
            "genuine_probability": round(
                genuine_percentage,
                2
            )
        }