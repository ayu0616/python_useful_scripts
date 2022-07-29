import cv2
import numpy as np
from PIL import Image

from white_outline import white_outline

img_path = input("image path => ")

img: np.ndarray = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
height, width, _ = img.shape

# 透明度情報がなかったらplusじゃないほうを実行する
if img.shape[2] == 3:
    white_outline(img_path)
elif np.all(img[:, :, 3] == 255):
    white_outline(img_path)
else:
    img = img[:, :, [2, 1, 0, 3]]
    outline_width = int(min(width, height) * 2 / 100)  # 線の太さは縦横で短い方の2％
    # 画像を拡張する
    # 横から
    extend_horizontal = np.full((height, outline_width, 4), 0)
    img = np.append(img, extend_horizontal, axis=1)
    img = np.append(extend_horizontal, img, axis=1)
    # 続いて縦
    extend_vertical = np.full((outline_width, width + outline_width * 2, 4), 0)
    img = np.append(img, extend_vertical, axis=0)
    img = np.append(extend_vertical, img, axis=0)
    raw_img = img.copy()

    img[img[:, :, 3] != 0] = np.full(4, 255)
    for n in range(1, outline_width + 1):
        row_index, column_index = np.where(img[:, :, 3] != 0)
        for i in [-1, 1]:
            img[row_index + i, column_index] = np.full(4, 255)
            img[row_index, column_index + i] = np.full(4, 255)

    img = Image.fromarray(img.astype(np.uint8), mode="RGBA")
    raw_img = Image.fromarray(raw_img.astype(np.uint8), mode="RGBA")
    out_img = Image.alpha_composite(img, raw_img)
    out_img.save(img_path)
