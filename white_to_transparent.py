import cv2
import numpy as np
import re

img_path = input("img path => ")
img: np.ndarray = cv2.imread(img_path, -1)
height, width, color = img.shape
img = img.reshape(height * width, color)
img[np.all(img == 255, axis=1)] = 0
img = img.reshape(height, width, color)

out_path = re.sub(r"\..*$", ".png", img_path)
cv2.imwrite(img_path, img)
