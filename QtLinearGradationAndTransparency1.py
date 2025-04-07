"""
グラデーションと透明度を同時に変化させるには、`QColor`のアルファチャネル（透明度）をグラデーションの位置に応じて変化させます。以下に、線形グラデーションと放射状グラデーションの例を示します。

**1. 線形グラデーションと透明度:**

```python
"""
import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPainter, QBrush, QLinearGradient, QColor
from PyQt5.QtCore import QRect, QPointF

class LinearGradientAlphaExample(QWidget):
    def __init__(self):
        super().__init__()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # 線形グラデーションを作成
        gradient = QLinearGradient(QPointF(50, 50), QPointF(250, 250))

        # 透明度を変化させる
        gradient.setColorAt(0, QColor(255, 0, 0, 255))  # 開始点: 赤色、不透明
        gradient.setColorAt(1, QColor(0, 0, 255, 0))    # 終了点: 青色、透明

        # ブラシを作成し、グラデーションを設定
        brush = QBrush(gradient)
        painter.setBrush(brush)

        # 矩形を描画
        rect = QRect(50, 50, 300, 300)
        painter.drawRect(rect)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = LinearGradientAlphaExample()
    window.show()
    sys.exit(app.exec_())
