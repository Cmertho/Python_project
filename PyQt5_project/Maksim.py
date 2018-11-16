import sys
from PyQt5 import QtWidgets, QtGui, QtCore


class Main(QtWidgets.QWidget):
    items_select = 0

    def __init__(self):
        super().__init__()
        self.setStyleSheet("font-size: 24px;")
        label = QtWidgets.QLabel("Выберете личность")
        self.resize(500, 600)
        button_plus = QtWidgets.QPushButton()
        button_plus.clicked.connect(self.add_new_item)
        button_plus.setIcon(QtGui.QIcon("1.jpg"))
        button_plus.setDefault(False)
        button_plus.setFlat(True)
        button_plus.setIconSize(QtCore.QSize(51, 41))

        self.button_left = QtWidgets.QPushButton()
        self.button_left.setIcon(QtGui.QIcon("3.jpg"))
        self.button_left.setDefault(False)
        self.button_left.setFlat(True)
        self.button_left.setIconSize(QtCore.QSize(51, 41))
        self.button_left.clicked.connect(lambda: self.next_items(0))

        self.button_right = QtWidgets.QPushButton()
        self.button_right.setIcon(QtGui.QIcon("2.jpg"))
        self.button_right.setDefault(False)
        self.button_right.setFlat(True)
        self.button_right.setIconSize(QtCore.QSize(51, 41))
        self.button_right.clicked.connect(lambda: self.next_items(1))

        self.button_left.setVisible(False)
        self.button_right.setVisible(False)

        layout_left_and_right = QtWidgets.QHBoxLayout()
        layout_left_and_right.addWidget(self.button_left, 1, QtCore.Qt.AlignRight | QtCore.Qt.AlignBottom)
        layout_left_and_right.addWidget(self.button_right, 0, QtCore.Qt.AlignRight | QtCore.Qt.AlignBottom)

        self.list_widget = QtWidgets.QListWidget()
        self.list_widget.itemClicked.connect(self.items_clicked)
        self.list_widget.setStyleSheet("""
            QListWidget{
                background: #F0F0F0;
                border:0px;
            }
            QListWidget::item{
                padding: 25px;
                border: 1px outset black;
            }
            QListWidget::item:selected{
                    color: #000;
                }
        """)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(label, 0, QtCore.Qt.AlignCenter)
        layout.addWidget(self.list_widget)
        layout.addLayout(layout_left_and_right)
        layout.addWidget(button_plus, 0, QtCore.Qt.AlignBottom | QtCore.Qt.AlignRight)
        self.setLayout(layout)

    def add_new_item(self):
        file, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open File", "/")
        if file:
            self.list_widget.clear()
            self.items_select = 0
            with open(file) as file:
                self.items_file = file.read().split(",")
            if len(self.items_file) > 4:
                self.list_widget.addItems(self.items_file[self.items_select:self.items_select + 4])
                self.button_right.setVisible(True)
            else:
                self.list_widget.addItems(self.items_file)
                self.button_left.setVisible(False)
                self.button_right.setVisible(False)

    def next_items(self, side):
        self.list_widget.clear()
        if side:
            if len(self.items_file) < self.items_select + 4:
                self.list_widget.addItems(self.items_file[self.items_select:])
                self.button_right.setVisible(False)
            else:
                self.items_select += 4
                self.list_widget.addItems(self.items_file[self.items_select:self.items_select + 4])
                if len(self.items_file) < self.items_select + 5:
                    self.button_right.setVisible(False)
            self.button_left.setVisible(True)
        else:
            if 0 > self.items_select - 4:
                self.list_widget.addItems(self.items_file[0:4])
                self.button_left.setVisible(False)
                self.items_select = 0
            else:
                self.items_select -= 4
                self.list_widget.addItems(self.items_file[self.items_select:self.items_select + 4])
                if 0 > self.items_select - 4:
                    self.button_left.setVisible(False)
            self.button_right.setVisible(True)

    def items_clicked(self, items):
        self.name = items.text()
        self.custom = Custom(self, self.name)
        self.custom.exec()


class Custom(QtWidgets.QDialog):
    def __init__(self, parent=None, item=None, *args, **kwargs):
        super(Custom, self).__init__(parent,  *args, **kwargs)
        self.label = QtWidgets.QLabel(item)
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main = Main()
    main.show()
    sys.exit(app.exec_())
 
 
 # -------------------------------------------------------
 import sys
from PyQt5 import QtWidgets, QtGui, QtCore


class Main(QtWidgets.QWidget):
    items_select = 0
    name = ""

    def __init__(self):
        super().__init__()
        self.setStyleSheet("font-size: 24px;")
        label = QtWidgets.QLabel("Выберете личность")
        self.resize(500, 600)
        button_plus = QtWidgets.QPushButton()
        button_plus.clicked.connect(self.add_new_item)
        button_plus.setIcon(QtGui.QIcon("1.jpg"))
        button_plus.setDefault(False)
        button_plus.setFlat(True)
        button_plus.setIconSize(QtCore.QSize(51, 41))

        self.button_left = QtWidgets.QPushButton()
        self.button_left.setIcon(QtGui.QIcon("3.jpg"))
        self.button_left.setDefault(False)
        self.button_left.setFlat(True)
        self.button_left.setIconSize(QtCore.QSize(51, 41))
        self.button_left.clicked.connect(lambda: self.next_items(0))

        self.button_right = QtWidgets.QPushButton()
        self.button_right.setIcon(QtGui.QIcon("2.jpg"))
        self.button_right.setDefault(False)
        self.button_right.setFlat(True)
        self.button_right.setIconSize(QtCore.QSize(51, 41))
        self.button_right.clicked.connect(lambda: self.next_items(1))

        self.button_left.setVisible(False)
        self.button_right.setVisible(False)

        layout_left_and_right = QtWidgets.QHBoxLayout()
        layout_left_and_right.addWidget(self.button_left, 1, QtCore.Qt.AlignRight | QtCore.Qt.AlignBottom)
        layout_left_and_right.addWidget(self.button_right, 0, QtCore.Qt.AlignRight | QtCore.Qt.AlignBottom)

        self.list_widget = QtWidgets.QListWidget()
        self.list_widget.itemClicked.connect(self.items_clicked)
        self.list_widget.setStyleSheet("""
            QListWidget{
                background: #F0F0F0;
                border:0px;
            }
            QListWidget::item{
                padding: 25px;
                border: 1px outset black;
            }
            QListWidget::item:selected{
                    color: #000;
                }
        """)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(label, 0, QtCore.Qt.AlignCenter)
        layout.addWidget(self.list_widget)
        layout.addLayout(layout_left_and_right)
        layout.addWidget(button_plus, 0, QtCore.Qt.AlignBottom | QtCore.Qt.AlignRight)
        self.setLayout(layout)

    def add_new_item(self):
        file, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open File", "/")
        if file:
            self.list_widget.clear()
            self.items_select = 0
            with open(file) as file:
                self.items_file = file.read().split(",")
            if len(self.items_file) > 4:
                self.list_widget.addItems(self.items_file[self.items_select:self.items_select + 4])
                self.button_right.setVisible(True)
            else:
                self.list_widget.addItems(self.items_file)
                self.button_left.setVisible(False)
                self.button_right.setVisible(False)

    def next_items(self, side):
        self.list_widget.clear()
        if side:
            if len(self.items_file) < self.items_select + 4:
                self.list_widget.addItems(self.items_file[self.items_select:])
                self.button_right.setVisible(False)
            else:
                self.items_select += 4
                self.list_widget.addItems(self.items_file[self.items_select:self.items_select + 4])
                if len(self.items_file) < self.items_select + 5:
                    self.button_right.setVisible(False)
            self.button_left.setVisible(True)
        else:
            if 0 > self.items_select - 4:
                self.list_widget.addItems(self.items_file[0:4])
                self.button_left.setVisible(False)
                self.items_select = 0
            else:
                self.items_select -= 4
                self.list_widget.addItems(self.items_file[self.items_select:self.items_select + 4])
                if 0 > self.items_select - 4:
                    self.button_left.setVisible(False)
            self.button_right.setVisible(True)

    def items_clicked(self, items):
        self.name = items.text()
        self.custom = Custom(self)
        self.custom.exec()


class Custom(QtWidgets.QDialog):
    def __init__(self, parent=None, *args, **kwargs):
        super(Custom, self).__init__(parent,  *args, **kwargs)
        self.label = QtWidgets.QLabel(parent.name)
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main = Main()
    main.show()
    sys.exit(app.exec_())
