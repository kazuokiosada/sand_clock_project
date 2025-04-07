"""
PyQtで折れ線を表示するには、`QPainter`クラスの`drawPolyline()`メソッドを使用します。`drawPolyline()`メソッドは、`QPoint`オブジェクトのリストを受け取り、それらの点を結ぶ折れ線を描画します。

以下に、PyQtで折れ線を表示する例を示します。

```python
"""
import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtCore import Qt, QPoint

class Example(QWidget):
    def paintEvent(self, event):
        painter = QPainter(self)

        # 折れ線の点を定義
        points = [
            QPoint(50, 50),
            QPoint(150, 100),
            QPoint(250, 50),
            QPoint(350, 150),
            QPoint(450, 100)
        ]

        # ペンの設定
        pen = QPen(QColor('blue'))
        pen.setWidth(3)
        painter.setPen(pen)

        # 折れ線を描画
        painter.drawPolyline(points)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Example()
    window.show()
    sys.exit(app.exec_())
"""
```

**コードの説明:**

1.  `QPainter`オブジェクトを作成します。
2.  `QPoint`オブジェクトのリストを作成し、折れ線の点を定義します。
3.  `QPen`オブジェクトを作成し、ペンの色と太さを設定します。
4.  `painter.setPen()`メソッドで、ペンを`QPainter`に設定します。
5.  `painter.drawPolyline(points)`メソッドで、折れ線を描画します。

**ポイント:**

* `QPoint`クラスは、整数座標で点を定義するためのクラスです。
* `QPointF`クラスを使用すると、浮動小数点数座標で点を定義できます。
* `drawPolyline()`メソッドは、点のリストを受け取り、それらの点を順番に結ぶ折れ線を描画します。
* ペンの色や太さを変更することで、折れ線のスタイルを変更できます。

**補足:**

* `drawLines()`メソッドを使用すると、点のペアを結ぶ複数の直線を描画できます。
* `drawPolygon()`メソッドを使用すると、点のリストで定義された多角形を描画できます。

この例を参考に、さまざまな折れ線を表示してみてください。
"""