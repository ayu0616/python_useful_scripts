from tkinter import filedialog, Tk
import os
from typing import Iterable, List, Callable, SupportsIndex, TypeVar, Union, overload
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
    def __init__(self, li: Iterable[T] = []):
        super().__init__(li)

    def filter(self, func: Callable[[T], bool]):
        return MyList(filter(func, self))

    def map(self, func: Callable[[T], S]) -> "MyList[S]":
        return MyList(map(func, self))

    def length(self):
        return self.__len__()

    def all_bool(self, func: Callable[[T], bool]):
        filtered = self.filter(func)
        return filtered.length() == self.length()

    def any_bool(self, func: Callable[[T], bool]):
        filtered = self.filter(func)
        return bool(filtered.length())

    def is_all_str(self):
        if not self.all_bool(lambda x: type(x) is str):
            raise TypeError("この配列に文字列ではない要素が含まれています")
        else:
            return True

    def match_filter(self: "MyList[str]", pattern: str, toggle_not=False):
        return self.filter(lambda x: bool(int(bool(re.match(pattern, x)))-int(toggle_not)))

    def sub(self: "MyList[str]", before: str, after: str):
        """
        文字列を置き換える\n
        re.sub()を使う
        """
        return self.map(lambda x: re.sub(before, after, x))

    def join(self, string: str):
        return string.join(self.map(str))

    def __add__(self, other: Iterable[T]):
        new_li = self
        for other_value in other:
            new_li.append(other_value)
        return new_li

    def __and__(self, other: Iterable[T]):
        new_li = self.filter(lambda x: x in other)
        return new_li

    def original(self):
        new_li = MyList()
        for value in self:
            if value not in new_li:
                new_li.append(value)
        return new_li

    def __or__(self, other: Iterable[T]):
        new_li = self
        for other_value in other:
            if other_value not in self:
                self.append(other_value)
        return new_li

    @overload
    def __getitem__(self, index: SupportsIndex) -> T:
        ...

    @overload
    def __getitem__(self, index: slice) -> "MyList[T]":
        ...

    def __getitem__(self, index: Union[SupportsIndex, slice]):
        if type(index) is int:
            item = super().__getitem__(index)
            return item
        elif type(index) is slice:
            items = MyList(super().__getitem__(index))
            return items
        else:
            raise Exception("slice / index が間違っています")

    def remove_all(self, x: T):
        while x in self:
            self.remove(x)


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


def my_glob(path: str, recursive: bool = False):
    return MyList(glob.glob(path, recursive=recursive))


def read_text_file(path: str):
    with open(path, "r") as f:
        text = f.read()
    return text
