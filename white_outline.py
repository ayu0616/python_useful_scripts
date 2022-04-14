from PIL import Image, ImageDraw
# from helper import get_file_path
import math


def white_outline(fname: str):
    waku_color = (255, 255, 255)  # 枠線の色（RGB）

    # 元になる画像からImageオブジェクトを作成
    src_im = Image.open(fname)
    sw, sh = src_im.size  # 元の画像のサイズを取得
    line_width = math.floor(min(sw, sh) * 0.02)  # line width（枠線一本の幅：画像サイズの短い長さの2％）

    # キャンバスを作成
    # この画像に枠線と元の画像を合成する
    cw, ch = sw + line_width * 2, sh + line_width * 2  # キャンバスのサイズを元の画像から生成
    canvas_im = Image.new('RGB', (cw, ch))

    # キャンバスのImageDrawオブジェクトを作成
    canvas = ImageDraw.Draw(canvas_im)

    # キャンバスを単色で塗りつぶす
    canvas.rectangle([(0, 0), (cw, ch)], fill=waku_color)

    # キャンバスの画像に元の画像を貼り付け
    canvas_im.paste(src_im, (line_width, line_width))

    # 保存
    canvas_im.save(fname)


if __name__ == "__main__":
    fname = input("file path => ")
    white_outline(fname)
