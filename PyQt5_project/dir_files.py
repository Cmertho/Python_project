import sys
import os
from PyQt5 import QtWidgets, QtCore

__author__ = "Twiss"


class ListWidget(QtWidgets.QListWidget):
    label = QtCore.pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setStyleSheet("""
            QListWidget{
                background: white;
                font-size: 18px;
                font-family: Aria;
                color: black;
                border: 0px;
            }
            QListWidget::item:selected:active {
                color: black;
            }
            QListWidget::item:hover {
                background-color: rgba(255, 255 , 255, 0);
                color: #000;
            }
            QListWidget::item:!hover {
                background-color: rgba(255, 255 , 255, 0);
                color: #000;
            }
            QPushButton{
                background: white;
                font-size: 18px;
                font-family: Aria;
                padding: 5px;
                color: black;
                border: 0px;
                text-align: left;
            }
            QLabel{
                font-size: 15px;
                font-style: Time New Roman;
            }
        """)

        self.setSpacing(5)
        button_item = QtWidgets.QListWidgetItem()
        button_back = QtWidgets.QPushButton("...")
        button_back.clicked.connect(lambda: self.open_file("..."))
        self.addItem(button_item)
        self.setItemWidget(button_item, button_back)

        self.addItems(os.listdir(os.getcwd()))
        self.itemDoubleClicked.connect(self.open_file)

    def open_file(self, text=""):
        list_dir = ""
        if isinstance(text, QtWidgets.QListWidgetItem):
            file_start, file_end = os.path.splitext(text.text())
        else:
            file_start, file_end = os.path.splitext(text)

        file_name = file_start + file_end
        if any([file_start == "...", os.path.isdir(file_name)]):

            if file_start == "...":
                file_dir = os.getcwd().split("\\")
                del file_dir[-1]
                if len(file_dir) == 1:
                    os.chdir(f"{file_dir[0]}\\")
                else:
                    os.chdir("\\".join(file_dir))
                list_dir = os.listdir(os.getcwd())

            elif os.path.isdir(file_name):
                try:
                    list_dir = os.listdir(os.getcwd() + f"/{file_name}")
                    os.chdir(file_name)
                except PermissionError:
                    return QtWidgets.QMessageBox.critical(self, "PermissionError", "Недостаточно прав",
                                                          QtWidgets.QMessageBox.Ok)
            self.clear()
            button_item = QtWidgets.QListWidgetItem()
            button_back = QtWidgets.QPushButton("...")
            button_back.clicked.connect(lambda: self.open_file("..."))
            self.addItem(button_item)
            self.setItemWidget(button_item, button_back)
            self.addItems(list_dir)

        elif os.path.isfile(file_name):
            os.startfile(file_name)
        self.label.emit()


class Panel(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.resize(600, 600)
        self.setStyleSheet("""
            QLabel{
                font: 16px Times New Roman bold;
            }
        """)
        self.list_widget = ListWidget()
        
        self.label = QtWidgets.QLabel(os.getcwd())
        self.list_widget.label.connect(lambda: self.label.setText(os.getcwd()))

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.list_widget)
        self.setLayout(layout)

 
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main = Panel()
    main.show()
    sys.exit(app.exec_())
