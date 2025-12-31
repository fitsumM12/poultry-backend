# ml/models.py
import os
import tensorflow as tf
from tensorflow.keras.layers import (
    Input, Dense, GlobalAveragePooling2D, Dropout
)
from tensorflow.keras.models import Model
from django.conf import settings


# =========================
# CREATE MODEL (EfficientNet)
# =========================
# def create_model(num_classes=3, img_size=224):
#     inputs = Input(shape=(img_size, img_size, 3), name="input_image")

#     base_model = tf.keras.applications.EfficientNetB0(
#         input_tensor=inputs,
#         weights="imagenet",
#         include_top=False
#     )

#     # Freeze backbone (optional but recommended for inference)
#     base_model.trainable = False

#     x = base_model.output
#     x = GlobalAveragePooling2D(name="gap")(x)
#     x = Dense(128, activation="relu")(x)
#     x = Dropout(0.3)(x)

#     outputs = Dense(num_classes, activation="softmax")(x)

#     model = Model(inputs=inputs, outputs=outputs, name="BroilerDiseaseEfficientNet")
#     return model


# =========================
# CREATE MODEL (MobileNetV2)
# ==========================
def create_model(num_classes=3, img_size=224):
        inputs = Input(shape=(img_size, img_size, 3), name="input_image")

        base_model = tf.keras.applications.mobilenetv2(
            input_tensor=inputs,
            weights="imagenet",
            include_top=False, alpha=0.35
        )

        # Freeze backbone (optional but recommended for inference)
        # base_model.trainable = False

        x = base_model.get_layer('block7a_project_conv').output
        x = GlobalAveragePooling2D(name='gap')(x)
        output = Dense(3,activation='softmax')(x)
        model = tf.keras.Model(inputs,output)
        return model

# # =========================
# # LOAD TRAINED WEIGHTS
# # =========================
# def load_weights(model):
#     """
#     Place your trained EfficientNet weights inside:
#     MEDIA_ROOT_MODEL/broiler_efficientnet.h5
#     """
#     weights_path = os.path.join(
#         settings.MEDIA_ROOT_MODEL,
#         "broiler_efficientnet.h5"
#     )
#     model.load_weights(weights_path)


# =========================
# LOAD TRAINED WEIGHTS
# =========================
def load_weights(model):
    """
    Place your trained MobileNetV2 weights inside:
    MEDIA_ROOT_MODEL/EfficientNet.h5
    """
    weights_path = os.path.join(
        settings.MEDIA_ROOT_MODEL,
        "broiler_model_tf"
    )
    model.load_weights(weights_path)


# =========================
# # PREDICT
# # =========================
# def predict(model, image_data):
#     """
#     image_data shape: (1, 224, 224, 3)
#     """
#     image_data = tf.keras.applications.efficientnet.preprocess_input(image_data)
#     predictions = model.predict(image_data)
#     return predictions
# PREDICT
# =========================
def predict(model, image_data):
    """
    image_data shape: (1, 224, 224, 3)
    """
    image_data = tf.keras.applications.mobilenetv2.preprocess_input(image_data)
    predictions = model.predict(image_data)
    return predictions
