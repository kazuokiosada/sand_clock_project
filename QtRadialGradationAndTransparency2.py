"""
**2. 放射状グラデーションと透明度:**

```python
"""
import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPainter, QBrush, QRadialGradient, QColor
from PyQt5.QtCore import QRect, QPointF

class RadialGradientAlphaExample(QWidget):
    def __init__(self):
        super().__init__()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # 放射状グラデーションを作成
        center = QPointF(200, 200)
        radius = 150
        gradient = QRadialGradient(center, radius)

        # 透明度を変化させる
        gradient.setColorAt(0, QColor(255, 255, 255, 255))  # 中心: 白色、不透明
        gradient.setColorAt(1, QColor(128, 128, 128, 0))    # 外側: 灰色、透明

        # ブラシを作成し、グラデーションを設定
        brush = QBrush(gradient)
        painter.setBrush(brush)

        # 円を描画
        rect = QRect(50, 50, 300, 300)
        painter.drawEllipse(rect)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = RadialGradientAlphaExample()
    window.show()
    sys.exit(app.exec_())
"""
```

**コードの説明:**

* `QColor(r, g, b, a)`の`a`はアルファチャネルを表し、0から255の範囲で透明度を指定します。0は完全に透明、255は完全に不透明です。
* `setColorAt()`メソッドでグラデーションの色と位置を設定する際に、アルファチャネルを変化させることで、グラデーションに透明度の変化を加えることができます。

これらの例では、線形グラデーションと放射状グラデーションの両方で、透明度を変化させています。必要に応じて、グラデーションの種類や色の変化、透明度の変化を調整してください。
"""