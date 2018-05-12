import sys
from PyQt5 import QtCore, QtWidgets, QtGui


class NameClass(QtWidgets.QWidget):
    text_name = QtCore.pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.Tool | QtCore.Qt.WindowStaysOnTopHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        label = QtWidgets.QLabel()
        self.text_name.connect(label.setText)
        label.setStyleSheet("""QLabel { color : #fff; 
                                       margin-top: 6px;
                                       margin-bottom: 6px;
                                       margin-left: 10px;
                                       margin-right: 10px; 
                                       font-size: 50px;}""")
        lay = QtWidgets.QVBoxLayout()
        lay.addWidget(label)
        self.setLayout(lay)
        self.adjustSize()
        self.animation = QtCore.QPropertyAnimation(self, b"windowOpacity", self)
        self.animation.finished.connect(self.hide)
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.hideAnimation)

    def paintEvent(self, event: QtGui.QPaintEvent):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        rounded_rect = QtCore.QRect()
        rounded_rect.setX(self.rect().x() + 5)
        rounded_rect.setY(self.rect().y() + 5)
        rounded_rect.setWidth(self.rect().width() - 10)
        rounded_rect.setHeight(self.rect().height() - 10)
        painter.setBrush(QtGui.QBrush(QtGui.QColor(0, 0, 0, 180)))
        painter.setPen(QtCore.Qt.NoPen)
        painter.drawRoundedRect(rounded_rect, 10, 10)

    def mouseDoubleClickEvent(self, event):
        print('asd')

    def show(self):
        self.setWindowOpacity(0.0)
        self.animation.setDuration(1500)
        self.animation.setStartValue(0.0)
        self.animation.setEndValue(1.0)
        QtWidgets.QWidget.show(self)
        self.animation.start()
        self.timer.start(5000)

    def hideAnimation(self):
        self.timer.stop()
        self.animation.setDuration(1500)
        self.animation.setStartValue(1.0)
        self.animation.setEndValue(0.0)
        self.animation.start()

    def hide(self):
        if self.windowOpacity() == 0:
            QtWidgets.QWidget.hide(self)


class Main(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.line = QtWidgets.QLineEdit()

        a = QtWidgets.QPushButton("Нажми")
        a.clicked.connect(self.a)
        lay = QtWidgets.QVBoxLayout()
        lay.addWidget(self.line)
        lay.addWidget(a)
        self.setLayout(lay)

    def a(self):
        name = NameClass()
        name.text_name.emit(self.line.text())
        name.show()
        self.position(name)

    def position(self, win):
        screen_geometry = QtWidgets.QApplication.desktop().availableGeometry()
        screen_size = (screen_geometry.width(), screen_geometry.height())
        win_size = (win.frameSize().width(), win.frameSize().height())
        x = screen_size[0] - win_size[0] - 10
        y = screen_size[1] - win_size[1] - 10
        win.move(x, y)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = Main()
    w.show()
    sys.exit(app.exec_())
