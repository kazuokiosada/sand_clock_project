"""
色を選択させる方法は、使用する環境やプログラミング言語によって異なります。ここでは、代表的な方法をいくつか紹介します。
**1. グラフィカルユーザーインターフェース (GUI) ツールキットを使用する方法***
 **PyQt (Python):**
    * `QColorDialog` クラスを使用して、色選択ダイアログを表示できます。
    ```python
"""
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QColorDialog
from PyQt5.QtGui import QColor
import sys

class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        btn = QPushButton('色を選択', self)
        btn.move(20, 20)
        btn.clicked.connect(self.showColorDialog)

        self.setGeometry(300, 300, 250, 180)
        self.setWindowTitle('色選択')
        self.show()

    def showColorDialog(self):
        col = QColorDialog.getColor()

        if col.isValid():
            print(f"選択された色: {col.getRgb()}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
