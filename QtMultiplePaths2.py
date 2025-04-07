"""
**2. パス演算:**

この例では、パス演算（交差、和、差など）を使用して、複雑な図形を作成します。

```python
"""
import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPainter, QPainterPath, QPolygonF
from PyQt5.QtCore import Qt, QPointF

class PathOperations(QWidget):
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # 1つ目のパス: 矩形
        path1 = QPainterPath()
        path1.addRect(50, 50, 150, 100)

        # 2つ目のパス: 楕円
        path2 = QPainterPath()
        path2.addEllipse(100, 100, 150, 100)

        # パス演算: 交差
        intersection_path = path1.intersected(path2)

        # パス演算の結果を描画
        painter.drawPath(intersection_path)

if __name__ == '__main__':
    print("パス演算（交差、和、差など）を使用")
    app = QApplication(sys.argv)
    window = PathOperations()
    window.show()
    sys.exit(app.exec_())
