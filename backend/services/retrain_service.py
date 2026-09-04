import os
import shutil
from datetime import datetime

import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import load_model


IMG_SIZE = 128


class SignatureRetrainer:

    def __init__(
        self,
        model_path,
        forged_dir,
        genuine_dir,
        backup_dir
    ):
        self.model_path = model_path
        self.forged_dir = forged_dir
        self.genuine_dir = genuine_dir
        self.backup_dir = backup_dir

    # ---------------------------------------------------------
    # Utility methods
    # ---------------------------------------------------------

    def _valid_images(self, directory):

        if not os.path.exists(directory):
            return []

        valid_extensions = (
            ".jpg",
            ".jpeg",
            ".png",
            ".webp"
        )

        files = []

        for filename in os.listdir(directory):

            full_path = os.path.join(
                directory,
                filename
            )

            if (
                os.path.isfile(full_path)
                and filename.lower().endswith(
                    valid_extensions
                )
            ):
                files.append(full_path)

        return sorted(files)

    def _validate_dataset(self):

        forged_images = self._valid_images(
            self.forged_dir
        )

        genuine_images = self._valid_images(
            self.genuine_dir
        )

        if len(forged_images) == 0:
            raise ValueError(
                "No forged signature images found."
            )

        if len(genuine_images) == 0:
            raise ValueError(
                "No genuine signature images found."
            )

        return forged_images, genuine_images

    # ---------------------------------------------------------
    # Model backup
    # ---------------------------------------------------------

    def _backup_model(self):

        if not os.path.exists(
            self.model_path
        ):
            raise FileNotFoundError(
                f"Model not found: {self.model_path}"
            )

        os.makedirs(
            self.backup_dir,
            exist_ok=True
        )

        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )

        backup_filename = (
            f"signature_model_{timestamp}.keras"
        )

        backup_path = os.path.join(
            self.backup_dir,
            backup_filename
        )

        shutil.copy2(
            self.model_path,
            backup_path
        )

        return backup_path

    # ---------------------------------------------------------
    # Validation dataset
    # ---------------------------------------------------------

    def _create_validation_dataset(
        self,
        forged_images,
        genuine_images,
        validation_root
    ):

        if os.path.exists(
            validation_root
        ):
            shutil.rmtree(
                validation_root
            )

        forged_validation_dir = os.path.join(
            validation_root,
            "forged"
        )

        genuine_validation_dir = os.path.join(
            validation_root,
            "genuine"
        )

        os.makedirs(
            forged_validation_dir,
            exist_ok=True
        )

        os.makedirs(
            genuine_validation_dir,
            exist_ok=True
        )

        # Use approximately 20% for validation.
        # Always use at least one image when possible.
        forged_validation_count = max(
            1,
            int(len(forged_images) * 0.2)
        )

        genuine_validation_count = max(
            1,
            int(len(genuine_images) * 0.2)
        )

        forged_validation = forged_images[
            :forged_validation_count
        ]

        genuine_validation = genuine_images[
            :genuine_validation_count
        ]

        for source_path in forged_validation:

            destination_path = os.path.join(
                forged_validation_dir,
                os.path.basename(source_path)
            )

            shutil.copy2(
                source_path,
                destination_path
            )

        for source_path in genuine_validation:

            destination_path = os.path.join(
                genuine_validation_dir,
                os.path.basename(source_path)
            )

            shutil.copy2(
                source_path,
                destination_path
            )

        return (
            forged_validation_dir,
            genuine_validation_dir
        )

    # ---------------------------------------------------------
    # Retraining
    # ---------------------------------------------------------

    def retrain(
        self,
        epochs=10,
        batch_size=32
    ):

        (
            forged_images,
            genuine_images
        ) = self._validate_dataset()

        # -----------------------------------------------------
        # Backup existing model
        # -----------------------------------------------------

        backup_path = self._backup_model()

        validation_root = os.path.join(
            os.path.dirname(
                os.path.dirname(
                    self.forged_dir
                )
            ),
            "validation_temp"
        )

        temporary_model_path = (
            self.model_path
            + ".temp.keras"
        )

        try:

            # -------------------------------------------------
            # Create temporary validation dataset
            # -------------------------------------------------

            (
                forged_validation_dir,
                genuine_validation_dir
            ) = self._create_validation_dataset(
                forged_images,
                genuine_images,
                validation_root
            )

            # -------------------------------------------------
            # IMPORTANT:
            # Binary sigmoid model
            # -------------------------------------------------
            #
            # Directory structure:
            #
            # train/
            #   forged/
            #   genuine/
            #
            # Keras alphabetical class mapping:
            #
            # forged  = 0
            # genuine = 1
            #
            # class_mode="binary" returns:
            #
            # forged  -> 0
            # genuine -> 1
            #
            # This matches:
            #
            # Dense(1, activation="sigmoid")
            # -------------------------------------------------

            train_datagen = ImageDataGenerator(
                rescale=1.0 / 255.0,
                rotation_range=10,
                width_shift_range=0.1,
                height_shift_range=0.1,
                shear_range=0.1,
                zoom_range=0.1,
                horizontal_flip=False,
                fill_mode="nearest"
            )

            validation_datagen = ImageDataGenerator(
                rescale=1.0 / 255.0
            )

            train_generator = (
                train_datagen.flow_from_directory(
                    os.path.dirname(
                        self.forged_dir
                    ),
                    target_size=(
                        IMG_SIZE,
                        IMG_SIZE
                    ),
                    color_mode="grayscale",
                    batch_size=batch_size,
                    class_mode="binary",
                    shuffle=True
                )
            )

            validation_generator = (
                validation_datagen.flow_from_directory(
                    validation_root,
                    target_size=(
                        IMG_SIZE,
                        IMG_SIZE
                    ),
                    color_mode="grayscale",
                    batch_size=batch_size,
                    class_mode="binary",
                    shuffle=False
                )
            )

            # -------------------------------------------------
            # Load existing binary model
            # -------------------------------------------------

            model = load_model(
                self.model_path
            )

            # -------------------------------------------------
            # Compile as binary classifier
            # -------------------------------------------------

            model.compile(
                optimizer=tf.keras.optimizers.Adam(
                    learning_rate=0.0001
                ),
                loss="binary_crossentropy",
                metrics=[
                    "accuracy"
                ]
            )

            # -------------------------------------------------
            # Train
            # -------------------------------------------------

            history = model.fit(
                train_generator,
                validation_data=validation_generator,
                epochs=epochs,
                verbose=1
            )

            # -------------------------------------------------
            # Save retrained model to temporary .keras file
            # -------------------------------------------------

            model.save(
                temporary_model_path
            )

            # -------------------------------------------------
            # Replace old model only after successful training
            # -------------------------------------------------

            os.replace(
                temporary_model_path,
                self.model_path
            )

            # -------------------------------------------------
            # Get final metrics
            # -------------------------------------------------

            final_accuracy = None
            final_val_accuracy = None
            final_loss = None
            final_val_loss = None

            if history.history.get(
                "accuracy"
            ):
                final_accuracy = (
                    history.history[
                        "accuracy"
                    ][-1]
                )

            if history.history.get(
                "val_accuracy"
            ):
                final_val_accuracy = (
                    history.history[
                        "val_accuracy"
                    ][-1]
                )

            if history.history.get(
                "loss"
            ):
                final_loss = (
                    history.history[
                        "loss"
                    ][-1]
                )

            if history.history.get(
                "val_loss"
            ):
                final_val_loss = (
                    history.history[
                        "val_loss"
                    ][-1]
                )

            return {
                "success": True,
                "message": (
                    "Model retrained successfully."
                ),
                "epochs": epochs,
                "batch_size": batch_size,
                "forged_images": len(
                    forged_images
                ),
                "genuine_images": len(
                    genuine_images
                ),
                "backup_path": backup_path,
                "accuracy": (
                    round(
                        float(final_accuracy),
                        4
                    )
                    if final_accuracy is not None
                    else None
                ),
                "validation_accuracy": (
                    round(
                        float(
                            final_val_accuracy
                        ),
                        4
                    )
                    if final_val_accuracy is not None
                    else None
                ),
                "loss": (
                    round(
                        float(final_loss),
                        4
                    )
                    if final_loss is not None
                    else None
                ),
                "validation_loss": (
                    round(
                        float(final_val_loss),
                        4
                    )
                    if final_val_loss is not None
                    else None
                )
            }

        except Exception:

            # -------------------------------------------------
            # If retraining fails, restore the previous model
            # -------------------------------------------------

            if os.path.exists(
                temporary_model_path
            ):
                try:
                    os.remove(
                        temporary_model_path
                    )
                except OSError:
                    pass

            if os.path.exists(
                backup_path
            ):
                try:
                    shutil.copy2(
                        backup_path,
                        self.model_path
                    )
                except OSError:
                    pass

            raise

        finally:

            # -------------------------------------------------
            # Remove temporary validation dataset
            # -------------------------------------------------

            if os.path.exists(
                validation_root
            ):
                try:
                    shutil.rmtree(
                        validation_root
                    )
                except OSError:
                    pass