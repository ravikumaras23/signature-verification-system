import os
import shutil
from datetime import datetime

import tensorflow as tf

from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import load_model
from tensorflow.keras.callbacks import EarlyStopping


IMG_SIZE = 128
BATCH_SIZE = 16


class SignatureRetrainer:

    def __init__(
        self,
        model_path,
        dataset_path,
        backup_path
    ):
        self.model_path = model_path
        self.dataset_path = dataset_path
        self.backup_path = backup_path

    # -------------------------------------------------
    # Backup current model
    # -------------------------------------------------

    def backup_model(self):

        if not os.path.exists(
            self.model_path
        ):
            raise FileNotFoundError(
                "Current signature model was not found."
            )

        os.makedirs(
            self.backup_path,
            exist_ok=True
        )

        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )

        backup_file = os.path.join(
            self.backup_path,
            f"signature_model_{timestamp}.keras"
        )

        shutil.copy2(
            self.model_path,
            backup_file
        )

        return backup_file

    # -------------------------------------------------
    # Count images
    # -------------------------------------------------

    def count_images(
        self,
        folder
    ):

        if not os.path.exists(folder):
            return 0

        extensions = {
            ".png",
            ".jpg",
            ".jpeg",
            ".webp"
        }

        count = 0

        for filename in os.listdir(folder):

            path = os.path.join(
                folder,
                filename
            )

            if not os.path.isfile(path):
                continue

            extension = os.path.splitext(
                filename
            )[1].lower()

            if extension in extensions:
                count += 1

        return count

    # -------------------------------------------------
    # Validate dataset
    # -------------------------------------------------

    def validate_dataset(self):

        train_path = os.path.join(
            self.dataset_path,
            "train"
        )

        forged_path = os.path.join(
            train_path,
            "forged"
        )

        genuine_path = os.path.join(
            train_path,
            "genuine"
        )

        if not os.path.exists(
            forged_path
        ):

            raise FileNotFoundError(
                f"Missing folder: {forged_path}"
            )

        if not os.path.exists(
            genuine_path
        ):

            raise FileNotFoundError(
                f"Missing folder: {genuine_path}"
            )

        forged_count = self.count_images(
            forged_path
        )

        genuine_count = self.count_images(
            genuine_path
        )

        if forged_count == 0:

            raise ValueError(
                "No forged images found."
            )

        if genuine_count == 0:

            raise ValueError(
                "No genuine images found."
            )

        return {
            "forged": forged_count,
            "genuine": genuine_count,
            "total": (
                forged_count
                + genuine_count
            )
        }

    # -------------------------------------------------
    # Create temporary validation dataset
    # -------------------------------------------------

    def create_validation_dataset(
        self,
        validation_ratio=0.2
    ):

        train_path = os.path.join(
            self.dataset_path,
            "train"
        )

        validation_path = os.path.join(
            self.dataset_path,
            "_retrain_validation"
        )

        # Remove previous temporary validation set
        if os.path.exists(
            validation_path
        ):

            shutil.rmtree(
                validation_path
            )

        os.makedirs(
            validation_path,
            exist_ok=True
        )

        classes = [
            "forged",
            "genuine"
        ]

        validation_counts = {}

        for class_name in classes:

            source = os.path.join(
                train_path,
                class_name
            )

            destination = os.path.join(
                validation_path,
                class_name
            )

            os.makedirs(
                destination,
                exist_ok=True
            )

            files = []

            for filename in os.listdir(
                source
            ):

                path = os.path.join(
                    source,
                    filename
                )

                if not os.path.isfile(
                    path
                ):
                    continue

                extension = (
                    os.path.splitext(
                        filename
                    )[1]
                    .lower()
                )

                if extension in {
                    ".png",
                    ".jpg",
                    ".jpeg",
                    ".webp"
                }:

                    files.append(
                        filename
                    )

            # Deterministic shuffle
            files.sort()

            validation_count = max(
                1,
                int(
                    len(files)
                    * validation_ratio
                )
            )

            # Keep enough images for training
            if len(files) <= 2:
                validation_count = 1

            validation_files = files[
                :validation_count
            ]

            for filename in validation_files:

                shutil.copy2(
                    os.path.join(
                        source,
                        filename
                    ),
                    os.path.join(
                        destination,
                        filename
                    )
                )

            validation_counts[
                class_name
            ] = len(validation_files)

        return (
            validation_path,
            validation_counts
        )

    # -------------------------------------------------
    # Retrain model
    # -------------------------------------------------

    def retrain(
        self,
        epochs=10
    ):

        dataset_info = (
            self.validate_dataset()
        )

        # Backup old model first
        backup_file = (
            self.backup_model()
        )

        validation_path = None

        try:

            # Create temporary validation split
            (
                validation_path,
                validation_info
            ) = self.create_validation_dataset()

            train_path = os.path.join(
                self.dataset_path,
                "train"
            )

            # ---------------------------
            # Training generator
            # ---------------------------

            train_datagen = (
                ImageDataGenerator(
                    rescale=1.0 / 255.0,
                    rotation_range=10,
                    zoom_range=0.15,
                    shear_range=0.10
                )
            )

            # ---------------------------
            # Validation generator
            # ---------------------------

            validation_datagen = (
                ImageDataGenerator(
                    rescale=1.0 / 255.0
                )
            )

            train_data = (
                train_datagen.flow_from_directory(
                    train_path,
                    target_size=(
                        IMG_SIZE,
                        IMG_SIZE
                    ),
                    color_mode="grayscale",
                    batch_size=BATCH_SIZE,
                    class_mode="categorical",
                    shuffle=True
                )
            )

            validation_data = (
                validation_datagen
                .flow_from_directory(
                    validation_path,
                    target_size=(
                        IMG_SIZE,
                        IMG_SIZE
                    ),
                    color_mode="grayscale",
                    batch_size=BATCH_SIZE,
                    class_mode="categorical",
                    shuffle=False
                )
            )

            print(
                "Class mapping:",
                train_data.class_indices
            )

            # ---------------------------
            # Load existing model
            # ---------------------------

            model = load_model(
                self.model_path
            )

            # ---------------------------
            # Fine-tuning
            # ---------------------------

            model.compile(
                optimizer=tf.keras.optimizers.Adam(
                    learning_rate=0.00001
                ),
                loss="categorical_crossentropy",
                metrics=[
                    "accuracy"
                ]
            )

            early_stopping = (
                EarlyStopping(
                    monitor="val_loss",
                    patience=3,
                    restore_best_weights=True
                )
            )

            history = model.fit(
                train_data,
                validation_data=
                    validation_data,
                epochs=int(epochs),
                callbacks=[
                    early_stopping
                ]
            )

            # ---------------------------
            # Save temporary model
            # ---------------------------

            temporary_model = os.path.join(
                os.path.dirname(self.model_path),
                "signature_model_retrained_temp.keras"
            )

            model.save(
                temporary_model
            )   

            if not os.path.exists(
                temporary_model
            ):

                raise RuntimeError(
                    "New model was not created."
                )

            # ---------------------------
            # Replace old model
            # ---------------------------

            os.replace(
                temporary_model,
                self.model_path
            )

            accuracy = (
                history.history
                .get(
                    "accuracy",
                    [0]
                )[-1]
            )

            validation_accuracy = (
                history.history
                .get(
                    "val_accuracy",
                    [0]
                )[-1]
            )

            return {

                "dataset": dataset_info,

                "validation_dataset":
                    validation_info,

                "epochs_requested":
                    int(epochs),

                "epochs_completed":
                    len(
                        history.history[
                            "loss"
                        ]
                    ),

                "accuracy":
                    round(
                        float(
                            accuracy
                        ) * 100,
                        2
                    ),

                "validation_accuracy":
                    round(
                        float(
                            validation_accuracy
                        ) * 100,
                        2
                    ),

                "backup_model":
                    backup_file,

                "model":
                    self.model_path
            }

        finally:

            # Always remove temporary validation dataset
            if (
                validation_path
                and os.path.exists(
                    validation_path
                )
            ):

                shutil.rmtree(
                    validation_path
                )