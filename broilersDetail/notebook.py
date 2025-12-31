# {
#  "cells": [
#   {
#    "cell_type": "code",
#    "execution_count": null,
#    "metadata": {},
#    "outputs": [],
#    "source": [
#     "import tensorflow as tf\n",
#     "import numpy as np\n",
#     "from tensorflow.keras.preprocessing import image\n",
#     "import matplotlib.pyplot as plt\n",
#     "\n",
#     # "model_path = '/Users/Yehualashet/AIresearchCenter/CA/modified/folds/pruned_recompiled_xception_fold_1.h5'  # \n",
#     "model_path = r'C:\Users\yordi\OneDrive\Desktop\poultry\poultry-backend\media\modelweight\EfficientNet.h5'"

#     "model = tf.keras.models.load_model(model_path)\n",
#     "\n",
#     "img_path = '/Users/Yehualashet/AIresearchCenter/CA/data/HSIL/HSIL20.jpg' \n",
#     "img = image.load_img(img_path, target_size=(224, 224, 3))  \n",
#     "img_array = image.img_to_array(img)\n",
#     "img_array = np.expand_dims(img_array, axis=0)  \n",
#     "\n",
#     "datagen = tf.keras.preprocessing.image.ImageDataGenerator(rescale=1.0 / 255.0)\n",
#     "img_array = datagen.standardize(img_array)  # Rescale the image\n",
#     "\n",
#     "\n",
#     "predictions = model.predict(img_array)\n",
#     "\n",
#     "print(predictions)"
#    ]
#   }
#  ],
#  "metadata": {
#   "language_info": {
#    "name": "python"
#   }
#  },
#  "nbformat": 4,
#  "nbformat_minor": 2
# }
import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing import image

# Path to your model
model_path = r"C:\Poultry\Model\poultry1_model_tf"
model = tf.keras.models.load_model(model_path)
CLASS_NAMES = ["Newcastle", "Normal", "Other abnormal"]
# "C:\Poultry\Model\poultry1.h5"
# "C:\Poultry\Model\poultry1_model_tf"
img_path = r"C:\Poultry\po datasets\data\data\test\Newcastle\ncd.0.jpg_aug3.JPG"
img = image.load_img(img_path, target_size=(224, 224, 3))  # MobileNetV2 usually uses 224x224
img_array = image.img_to_array(img)
img_array = np.expand_dims(img_array, axis=0)

# Rescale the image
datagen = tf.keras.preprocessing.image.ImageDataGenerator(rescale=1.0 / 255.0)
img_array = datagen.standardize(img_array)

# Make prediction
# predictions = model(img_array)
# predictions = predictions.numpy()

# print(predictions)
