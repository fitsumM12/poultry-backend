import cv2
import numpy as np
from PIL import Image

def crop_image_from_gray(img, tol=7):
    if img.dtype != np.uint8:
        img = (255 * (img - np.min(img)) / (np.max(img) - np.min(img))).astype(np.uint8)
    if img.ndim == 2:
        mask = img > tol
        return img[np.ix_(mask.any(1), mask.any(0))]
    elif img.ndim == 3:
        gray_img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        mask = gray_img > tol
        if not mask.any():
            return img  
        img_cropped = img[np.ix_(mask.any(1), mask.any(0))]
        return img_cropped
    return img 

def apply_clahe(img):
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    img_clahe = np.empty_like(img)
    for i in range(img.shape[2]): 
        img_clahe[:, :, i] = clahe.apply(img[:, :, i])
    return img_clahe

def circle_crop(img, output_path=None):
    if isinstance(img, Image.Image):
        img = np.array(img)  
    img = crop_image_from_gray(img)
    if img.ndim == 3:
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    height, width, _ = img.shape    
    x = int(width / 2)
    y = int(height / 2)
    r = np.amin((x, y))
    circle_img = np.zeros((height, width), np.uint8)
    cv2.circle(circle_img, (x, y), r, 1, thickness=-1)
    img_cropped = cv2.bitwise_and(img, img, mask=circle_img)
    img_cropped = crop_image_from_gray(img_cropped)
    img_cropped = apply_clahe(img_cropped)
    img_cropped = cv2.cvtColor(img_cropped, cv2.COLOR_BGR2RGB)

    # Save image if output_path is provided
    if output_path:
        Image.fromarray(img_cropped).save(output_path+"/image.png")

    return img_cropped
