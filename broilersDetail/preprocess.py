import cv2
import numpy as np
import os
# from tensorflow.keras.applications.mobilenet_v2 import preprocess_input

labels = ["Newcastle", "Normal", "Other abnormal"]

def get_data(data_dir, img_size=224):
    x, y = [], []

    supported_extensions = ('.bmp', '.jpg', '.png')

    for label in os.listdir(data_dir):
        path = os.path.join(data_dir, label)
        class_num = labels.index(label)

        for img_name in os.listdir(path):
            if img_name.lower().endswith(supported_extensions):
                try:
                    img_path = os.path.join(path, img_name)

                    img_arr = cv2.imread(img_path)
                    img_arr = cv2.cvtColor(img_arr, cv2.COLOR_BGR2RGB)
                    resized_arr = cv2.resize(
                        img_arr, (img_size, img_size),
                        interpolation=cv2.INTER_LINEAR
                    )

                    x.append(resized_arr)
                    y.append(class_num)

                except Exception as e:
                    print(f"Error loading {img_name}: {e}")

    # convert to array
    x = np.array(x, dtype=np.float32)

    # ✅ IMPORTANT — SAME preprocessing as backend
    # x = preprocess_input(x)

    y = np.array(y)

    return x, y
