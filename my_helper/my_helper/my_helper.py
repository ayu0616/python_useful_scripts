from tkinter import filedialog, Tk
import os
from typing import List, Callable, TypeVar, Union
import re
import cv2
import numpy as np
import glob


def get_file_path(initial_dir: str = os.path.dirname(__file__)):
    # ダイアログ用のルートウィンドウの作成
    root = Tk()
    # ウィンドウサイズを0にする（Windows用の設定）
    root.geometry("0x0")
    # ウィンドウのタイトルバーを消す（Windows用の設定）
    # root.overrideredirect(1)
    # ウィンドウを非表示に
    root.withdraw()
    root.update()
    # ダイアログを前面に
    root.lift()
    root.focus_force()
    # 動画プロジェクトのディレクトリ
    path = filedialog.askopenfilename(initialdir=initial_dir)
    root.update()
    # ディレクトリが選択されなかったらエラーを発生させる
    if not path:
        raise Exception("ファイルが選択されていません")
    return path


T = TypeVar("T")
S = TypeVar("S")


class MyList(List[T]):
    def __init__(self, li: Union[List[T], filter, map] = []):
        super().__init__(li)

    def filter(self, func: Callable[[T], bool]):
        return MyList(filter(func, self))

    def map(self, func: Callable[[T], S]):
        li: MyList[S] = MyList(map(func, self))
        return li

    def length(self):
        return self.__len__()

    def all_bool(self, func: Callable[[T], bool]):
        filtered = self.filter(func)
        return filtered.length() == self.length()

    def any_bool(self, func: Callable[[T], bool]):
        filtered = self.filter(func)
        return bool(filtered.length())


class MyStringList(MyList[str]):
    def __init__(self, li: Union[List[str], filter, map] = []):
        super().__init__(li)

    def filter(self, func: Callable[[str], bool]):
        return MyStringList(filter(func, self))

    def map(self, func: Callable[[str], T]):
        mapped = map(func, self)
        if self.all_bool(lambda x: type(x) is str):
            li_str = MyStringList(mapped)
            return li_str
        else:
            li_any: MyList[T] = MyList(mapped)
            return li_any

    def match_filter(self, pattern: str, toggle_not=False):
        if toggle_not:
            return self.filter(lambda x: not re.match(pattern, x))
        else:
            return self.filter(lambda x: bool(re.match(pattern, x)))

    def sub(self, before: str, after: str):
        """
        文字列を置き換える
        re.sub()を使う
        """
        substituted: MyStringList = self.map(lambda x: re.sub(before, after, x))
        return substituted

    def join(self, string: str):
        return string.join(self.map(str))


def cut_by_content(img_path: str):
    """
    GIMPの「内容で切り抜き」をパクって作ってみた
    引数は画像のパス
    """
    img: np.ndarray = cv2.imread(img_path, -1)
    row_index, column_index = np.where(img[:, :, 3] != 0)
    up = min(row_index)
    down = max(row_index)
    left = min(column_index)
    right = max(column_index)
    cutted_img = img[up:down, left:right]
    cv2.imwrite(img_path, cutted_img)


def my_glob(path: str):
    return MyStringList(glob.glob(path))


def read_text_file(path: str):
    with open(path, "r") as f:
        text = f.read()
    return text
