import sys
import random
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPainter, QPolygon, QColor
from PyQt5.QtCore import Qt, QPoint, QTimer

class ShapeAnimation(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 400, 300)
        self.setWindowTitle('形状変化アニメーション')
        self.points = self.generateRandomShape()
        self.x_offset = 50
        self.direction = 1
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateShape)
        self.timer.start(50)
        self.show()

    def generateRandomShape(self):
        """ランダムな形状を生成"""
        points = []
        for _ in range(random.randint(3, 6)):  # 3～6個の頂点
            x = random.randint(0, 50)
            y = random.randint(0, 50)
            points.append(QPoint(x, y))
        return points

    def updateShape(self):
        self.x_offset += 5 * self.direction
        if self.x_offset > 350:
            self.direction = -1
            self.points = self.generateRandomShape()  # 形状を変化
        elif self.x_offset < 50:
            self.direction = 1
            self.points = self.generateRandomShape()  # 形状を変化
        self.update()

    def paintEvent(self, event):
        qp = QPainter(self)
        self.drawShape(qp)

    def drawShape(self, qp):
        translated_points = [p + QPoint(self.x_offset, 125) for p in self.points]
        polygon = QPolygon(translated_points)
        qp.setBrush(QColor(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
        qp.drawPolygon(polygon)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ShapeAnimation()
    sys.exit(app.exec_())