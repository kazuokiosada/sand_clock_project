"""
はい、複数の`QPainterPath`を使った例をいくつかご紹介します。複数の`QPainterPath`を組み合わせることで、複雑な図形や効果を実現できます。

**1. 複合図形の作成:**

この例では、複数の`QPainterPath`を組み合わせて、複雑な複合図形を作成します。

```python
"""
import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPainter, QPainterPath, QPolygonF
from PyQt5.QtCore import Qt, QPointF

class CompoundPath(QWidget):
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # 1つ目のパス: 円
        path1 = QPainterPath()
        path1.addEllipse(50, 50, 100, 100)

        # 2つ目のパス: 三角形
        path2 = QPainterPath()
        points = [QPointF(100, 10), QPointF(180, 150), QPointF(20, 150)]
        path2.addPolygon(QPolygonF(points))

        # 複合パスを作成
        compound_path = QPainterPath()
        compound_path.addPath(path1)
        compound_path.addPath(path2)

        # 複合パスを描画
        painter.drawPath(compound_path)

if __name__ == '__main__':
    print("複合図形の作成")
    app = QApplication(sys.argv)
    window = CompoundPath()
    window.show()
    sys.exit(app.exec_())
