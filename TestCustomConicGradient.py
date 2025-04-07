from PyQt5.QtGui import QGradient

class CustomConicalGradient(QGradient):
    def __init__(self):
        super().__init__()
        self.setType(QGradient.ConicalGradient)

gradient = CustomConicalGradient()