"""
`QColorDialog` でカスタムカラーをあらかじめ選択した状態で表示するには、`QColorDialog` のインスタンスを作成し、`setCurrentColor()` メソッドを使用して初期色を設定します。

以下に、具体的な手順とコード例を示します。

**手順:**

1.  `QColorDialog` のインスタンスを作成します。
2.  `QColor` オブジェクトを作成し、カスタムカラーのRGBA値を指定します。
3.  `QColorDialog` の `setCurrentColor()` メソッドを使用して、初期色を設定します。
4.  `QColorDialog` を表示します。

**コード例:**

```python
"""
import sys
from PyQt5.QtWidgets import QApplication, QColorDialog
from PyQt5.QtGui import QColor

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # カスタムカラーのRGBA値を指定してQColorオブジェクトを作成
    custom_color = QColor(255, 128, 0, 255)  # 例: オレンジ色

    # QColorDialogのインスタンスを作成
    # 初期色を設定
    color_dialog = QColorDialog(custom_color)

    # 初期色を設定
    ###color_dialog.setCurrentColor(custom_color)
    ###color_dialog.setCustomColor(0, custom_color)
    # ダイアログを表示
    color = color_dialog.getColor()

    # 色が選択された場合の処理
    if color.isValid():
        print("選択された色:", color.getRgb())

    sys.exit(app.exec_())
"""
```

**解説:**

* `QColor(255, 128, 0, 255)`: 赤(255)、緑(128)、青(0)、アルファ値(255)でオレンジ色の `QColor` オブジェクトを作成しています。
* `color_dialog.setCurrentColor(custom_color)`: `QColorDialog` の初期色を `custom_color` に設定しています。
* `color = color_dialog.getColor()`: `QColorDialog` を表示し、選択された色を取得しています。
* `color.isValid()`: 色が選択されたかどうかを確認しています。

このコードを実行すると、オレンジ色が初期選択された状態で `QColorDialog` が表示されます。ユーザーは、他の色を選択したり、カスタムカラーを調整したりできます。

**補足:**

* `QColorDialog` の `setOptions()` メソッドを使用すると、ダイアログのオプションを設定できます。例えば、`QColorDialog.ColorDialogOptions.ShowAlphaChannel` を設定すると、アルファチャンネルの調整が可能になります。
* `QColorDialog` の `setCustomColor(int index, QColor color)` メソッドを使用すると、カスタムカラーパレットに色を追加できます。
"""