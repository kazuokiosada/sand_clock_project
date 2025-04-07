"""
背景にグラデーション効果
ウインドウ枠なしで、マウスでつまんで動かす
"""
import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPainter, QColor, QBrush, QLinearGradient
from PyQt5.QtCore import Qt, QPoint

class GlassBottle(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.mouse_pressed = False
        self.mouse_pos = QPoint()

    def initUI(self):
        self.setGeometry(300, 300, 400, 600)
        self.setWindowTitle('透明なガラス瓶')
        self.setAttribute(Qt.WA_TranslucentBackground) # 背景を透明にする
        self.setWindowFlags(Qt.FramelessWindowHint) # 枠を非表示にする
        self.show()

    def paintEvent(self, event):
        qp = QPainter(self)
        qp.setRenderHint(QPainter.Antialiasing)
        self.drawBottle(qp)

    def drawBottle(self, qp):
        # ガラス瓶の形状を定義
        bottle_path = [
            QPoint(100, 50), QPoint(300, 50), QPoint(320, 550),
            QPoint(80, 550), QPoint(100, 50)
        ]

        # グラデーションの作成（ガラスの質感）
        gradient = QLinearGradient(100, 50, 320, 550)
        ###gradient.setColorAt(0, QColor(200, 200, 255, 100))  # 透明度を設定
        gradient.setColorAt(0, QColor(255, 255, 255, 0))  # 透明度を設定　全透明
        gradient.setColorAt(0.5, QColor(255, 255, 255, 255))###不透明
        ###gradient.setColorAt(1, QColor(255, 255, 255, 50))  # 透明度を設定
        gradient.setColorAt(1, QColor(255, 255, 255, 100))###半透明
        qp.setBrush(QBrush(gradient))

        # ガラス瓶の描画
        qp.drawPolygon(bottle_path)

        # 砂の描画（例として瓶の半分まで砂が入っている状態）
        sand_level = 300  # 砂の高さ
        sand_path = [
            QPoint(100, sand_level), QPoint(300, sand_level),
            QPoint(320, 550), QPoint(80, 550), QPoint(100, sand_level)
        ]
        qp.setBrush(QBrush(QColor(244, 164, 96)))  # 砂の色
        ###qp.drawPolygon(sand_path)
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.mouse_pressed = True
            self.mouse_pos = event.globalPos()
            event.accept()

    def mouseMoveEvent(self, event):
        if self.mouse_pressed:
            delta = event.globalPos() - self.mouse_pos
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.mouse_pos = event.globalPos()
            event.accept()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.mouse_pressed = False
            event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = GlassBottle()
    sys.exit(app.exec_())