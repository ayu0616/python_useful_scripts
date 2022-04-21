from PIL import Image
import os

in_img_path = input("image path => ")
in_img = Image.open(in_img_path)  # 白枠をつける画像

white_inline_img = Image.open(os.path.dirname(__file__)+"/sources/white_inline_1920p.png")  # 白枠の画像（内側15マスから25マスまで白枠）

in_img = in_img.convert("RGBA")
white_inline_img = white_inline_img.convert("RGBA")

out_img = Image.alpha_composite(in_img, white_inline_img)
out_img = out_img.convert("RGB")
out_img.save(in_img_path)
