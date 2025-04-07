"""
色を選択させる方法は、使用する環境やプログラミング言語によって異なります。ここでは、代表的な方法をいくつか紹介します。
**1. グラフィカルユーザーインターフェース (GUI) ツールキットを使用する方法***
* **Tkinter (Python):**
    * `colorchooser` モジュールを使用して、色選択ダイアログを表示できます。

    ```python
"""
import tkinter as tk
from tkinter import colorchooser

def choose_color():
    color_code = colorchooser.askcolor(title="色の選択")
    print(color_code)

root = tk.Tk()
button = tk.Button(root, text="色を選択", command=choose_color)
button.pack()
root.mainloop()
