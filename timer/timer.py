import sys
from PyQt5 import QtWidgets, QtCore, QtGui
__author__ = "Twiss"


class Times(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle("Timer")
        self.hours, self.minutes, self.seconds, self.value_image = 0, 0, 5, 0
        self.setWindowTitle('Таймер обратного отсчета')

        self.label_time = QtWidgets.QLabel('%02d : %02d : %02d' % (self.hours, self.minutes, self.seconds))
        self.label_time.setFont(QtGui.QFont("Times New Roman", 110))

        layout_button = QtWidgets.QHBoxLayout()
        self.button_start_time = QtWidgets.QPushButton("Начать отсчет")
        self.button_start_time.setFont(QtGui.QFont('Arial', 15))
        self.button_start_time.setShortcut('Alt+S')
        self.button_start_time.clicked.connect(lambda: self.timer.start(1000))

        self.button_stop_time = QtWidgets.QPushButton("Остановить отсчет")
        self.button_stop_time.setFont(QtGui.QFont('Arial', 15))
        self.button_stop_time.setShortcut('Alt+D')
        self.button_stop_time.clicked.connect(lambda: self.timer.stop())

        layout_button.addWidget(self.button_start_time)
        layout_button.addWidget(self.button_stop_time)

        layout_time = QtWidgets.QVBoxLayout()
        layout_time.addWidget(self.label_time, 0, QtCore.Qt.AlignCenter)
        layout_time.addLayout(layout_button)
        self.setLayout(layout_time)
        # main times
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.start_time)

    def start_time(self):

        if self.seconds == 0:
            if self.minutes == 0:
                if self.hours == 0:
                    self.label_time.setText('СТОП!')
                    self.timer.stop()
                else:
                    self.hours -= 1
                    self.minutes = 59
                    self.seconds = 59
            else:
                self.minutes -= 1
                self.seconds = 59
        else:
            self.seconds -= 1
        if self.label_time.text() == "СТОП!":
            pass
        else:
            self.label_time.setText('%02d : %02d : %02d' % (self.hours, self.minutes, self.seconds))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    root = Times()
    root.show()
    sys.exit(app.exec_())
