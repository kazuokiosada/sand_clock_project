"""
はい、図形を原点でない現在位置で拡大と回転を行う例を示します。

**考え方:**

1.  **移動:** まず、拡大と回転の中心となる座標に原点を移動します。
2.  **拡大と回転:** 移動後の原点を中心に、拡大と回転を行います。
3.  **移動 (逆方向):** 最後に、原点を元の位置に戻します。

**コード例:**

```python
"""
import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPainter, QPainterPath, QPolygonF, QTransform,QColor
from PyQt5.QtCore import Qt, QPointF

class ScaleRotateFromPoint(QWidget):
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # パスを作成 (例として三角形)
        path = QPainterPath()
        points = [QPointF(0, -50), QPointF(50, 50), QPointF(-50, 50)]
        path.addPolygon(QPolygonF(points))

        # 拡大と回転の中心となる座標
        center_x, center_y = 100, 100

        # 変換行列を作成
        transform = QTransform()
        transform.translate(center_x, center_y)  # 中心に移動
        transform.scale(2.0, 2.0)  # 拡大
        transform.rotate(45)  # 回転
        transform.translate(-center_x, -center_y)  # 原点に戻す

        # パスを変形して描画
        painter.setTransform(transform)
        painter.setBrush(QColor(255,0,0))
        painter.drawPath(path)

if __name__ == '__main__':
    print("図形を原点でない現在位置で拡大と回転を行う例")
    app = QApplication(sys.argv)
    window = ScaleRotateFromPoint()
    window.show()
    sys.exit(app.exec_())
"""
```

**コードの説明:**

1.  `translate(center_x, center_y)`: 拡大と回転の中心となる座標に原点を移動します。
2.  `scale(2.0, 2.0)`: 移動後の原点を中心に図形を拡大します。
3.  `rotate(45)`: 移動後の原点を中心に図形を 45 度回転します。
4.  `translate(-center_x, -center_y)`: 原点を元の位置 (0, 0) に戻します。

**ポイント:**

* 拡大と回転の順序は、`transform.scale()` と `transform.rotate()` の呼び出し順序によって決まります。
* この例では、拡大後に回転が行われます。
* `center_x` と `center_y` を変更することで、拡大と回転の中心座標を変更できます。

この例を参考に、さまざまな座標を基準とした図形の拡大と回転を試してみてください。
"""