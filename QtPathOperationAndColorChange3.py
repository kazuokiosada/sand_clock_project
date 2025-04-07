"""
**例3: 和 (united) と塗りつぶし**

```python
"""
import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPainter, QPainterPath, QColor, QBrush
from PyQt5.QtCore import Qt, QRectF

class PathUnion(QWidget):
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # 2つの矩形のパスを作成
        path1 = QPainterPath()
        path1.addRect(QRectF(50, 50, 100, 100))
        path2 = QPainterPath()
        path2.addRect(QRectF(100, 100, 100, 100))

        # 和演算
        union_path = path1.united(path2)

        # 塗りつぶしの設定
        brush = QBrush(QColor("green"))
        painter.setBrush(brush)

        # 和集合を塗りつぶして描画
        painter.drawPath(union_path)

if __name__ == '__main__':
    print("**例3: 和 (united) と塗りつぶし**")
    app = QApplication(sys.argv)
    window = PathUnion()
    window.show()
    sys.exit(app.exec_())
"""
```

この例では、2つの矩形を合わせた形状が緑色で塗りつぶされて表示されます。

これらの例からわかるように、パス演算は形状を操作し、その結果に対して塗りつぶしなどの描画設定を行うことで、さまざまな色の表現が可能になります。
"""