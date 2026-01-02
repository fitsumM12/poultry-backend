# predictor.py
import os
import tensorflow as tf
from django.conf import settings

# Path to your saved full model (.keras or SavedModel directory)
MODEL_PATH = r"C:\Poultry\Model\newmodel3.keras"

# Model class names
CLASS_NAMES = ["Newcastle", "Normal", "Other abnormal"]

# Global variable to hold the model after loading once
_model = None

def get_model():
    """
    Load the full model only once. 
    Returns the model instance for prediction.
    """
    global _model
    if _model is None:
        # Load the full Keras 3 model
        _model = tf.keras.models.load_model(MODEL_PATH, compile=False)
    return _model

def predict_image(img_array):
    """
    Predict the class for a preprocessed image array.
    
    img_array: numpy array of shape (1, 224, 224, 3)
    Returns: predicted class name and full predictions array
    """
    model = get_model()
    preds = model.predict(img_array)
    pred_index = int(tf.argmax(preds, axis=1)[0])
    return CLASS_NAMES[pred_index], preds
