"""
**例2: 差 (difference) と塗りつぶし**

```python
"""
import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPainter, QPainterPath, QColor, QBrush
from PyQt5.QtCore import Qt, QRectF

class PathDifference(QWidget):
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # 矩形と円のパスを作成
        path1 = QPainterPath()
        path1.addRect(QRectF(50, 50, 200, 200))
        path2 = QPainterPath()
        path2.addEllipse(QRectF(100, 100, 150, 150))

        # 差演算
        difference_path = path1.subtracted(path2)

        # 塗りつぶしの設定
        brush = QBrush(QColor("blue"))
        painter.setBrush(brush)

        # 差分を塗りつぶして描画
        painter.drawPath(difference_path)

if __name__ == '__main__':
    print("**例2: 差 (difference) と塗りつぶし**")
    app = QApplication(sys.argv)
    window = PathDifference()
    window.show()
    sys.exit(app.exec_())
"""
```

この例では、矩形から円をくり抜いた形状が青色で塗りつぶされて表示されます。
"""
