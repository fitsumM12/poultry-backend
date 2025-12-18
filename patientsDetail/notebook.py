{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "import tensorflow as tf\n",
    "import numpy as np\n",
    "from tensorflow.keras.preprocessing import image\n",
    "import matplotlib.pyplot as plt\n",
    "\n",
    "model_path = '/Users/Yehualashet/AIresearchCenter/CA/modified/folds/pruned_recompiled_xception_fold_1.h5'  # \n",
    "model = tf.keras.models.load_model(model_path)\n",
    "\n",
    "img_path = '/Users/Yehualashet/AIresearchCenter/CA/data/HSIL/HSIL20.jpg' \n",
    "img = image.load_img(img_path, target_size=(512, 512, 3))  \n",
    "img_array = image.img_to_array(img)\n",
    "img_array = np.expand_dims(img_array, axis=0)  \n",
    "\n",
    "datagen = tf.keras.preprocessing.image.ImageDataGenerator(rescale=1.0 / 255.0)\n",
    "img_array = datagen.standardize(img_array)  # Rescale the image\n",
    "\n",
    "\n",
    "predictions = model.predict(img_array)\n",
    "\n",
    "print(predictions)"
   ]
  }
 ],
 "metadata": {
  "language_info": {
   "name": "python"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
