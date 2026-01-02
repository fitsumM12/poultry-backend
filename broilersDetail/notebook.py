import tensorflow as tf
import numpy as np
# from tensorflow.keras.preprocessing import image

# notebook.py
import tensorflow as tf
import numpy as np

MODEL_PATH = r"C:\Poultry\Model\newmodel3.keras"  # or SavedModel directory
CLASS_NAMES = ["Newcastle", "Normal", "Other abnormal"]
_model = None  # model is not loaded yet

def get_model():
    """Load model only once, when first needed."""
    global _model
    if _model is None:
        _model = tf.keras.models.load_model(MODEL_PATH, compile=False)
    return _model

def predict_image(img_array):
    """Predict class for one image array (1,224,224,3)"""
    model = get_model()
    preds = model.predict(img_array)
    pred_index = np.argmax(preds, axis=1)[0]
    return CLASS_NAMES[pred_index], preds
