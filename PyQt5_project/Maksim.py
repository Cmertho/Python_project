import sys
from PyQt5 import QtWidgets


class Main(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        label = QtWidgets.QLabel("Какой то текст в окне которое надо закрыть")
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(label)
        self.setLayout(layout)
        self.dialog = Dialog()

    def closeEvent(self, QCloseEvent):
        self.dialog.show()
        super().close()


class Dialog(QtWidgets.QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        label = QtWidgets.QLabel("Какой то текст в новом окне")
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(label)
        self.setLayout(layout)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main = Main()
    main.show()
    sys.exit(app.exec_())
