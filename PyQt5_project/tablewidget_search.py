import sys
import os
from PyQt5 import QtWidgets, QtCore, QtGui


def log_uncaught_exceptions(ex_cls, ex, tb):
    text = '{}: {}:\n'.format(ex_cls.__name__, ex)
    import traceback
    text += ''.join(traceback.format_tb(tb))

    print(text)
    sys.exit(1)


sys.excepthook = log_uncaught_exceptions


class Table(QtWidgets.QTableWidget):
    dir_continue = [os.getcwd(), ]

    def __init__(self, parent: QtWidgets.QWidget=None):
        super().__init__(parent)
        self.main = parent
        self.main.back_clicked.connect(lambda: self.dir_select(0))
        self.main.continue_clicked.connect(lambda: self.dir_select(1))
        self.setColumnCount(4)
        self.setHorizontalHeaderLabels(["Название файла", "Размер файла", "Тип файла", "Путь файла"])
        self.add_items_table()
        self.itemDoubleClicked.connect(lambda x: self.item_connect(x))
        self.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.setSortingEnabled(True)


    def add_items_table(self):
        self.setRowCount(0)
        for i in self.add_file():
            self.insertRow(0)
            self.setItem(0, 0, QtWidgets.QTableWidgetItem(i[0]))
            self.setItem(0, 1, QtWidgets.QTableWidgetItem(i[1]))
            self.setItem(0, 2, QtWidgets.QTableWidgetItem(i[2]))
            self.setItem(0, 3, QtWidgets.QTableWidgetItem(i[3]))
        self.sortItems(2, QtCore.Qt.DescendingOrder)
        self.resizeColumnsToContents()

    @staticmethod
    def convert_size(num: int):
        for i in ['байтов', 'килобайтов', 'мегабайтов', 'гигобайтов', 'терабайтов']:
            if num < 1024.0:
                return "%3.1f %s" % (num, i)
            num /= 1024.0

    def add_file(self, dir_name: str=None):
        if dir_name is None:
            try:
                for i in os.listdir(os.getcwd()):
                    size_file = self.convert_size(os.stat(i).st_size)
                    file_start, file_end = os.path.splitext(i)
                    if file_end == "":
                        file_end = "Папка"
                    file_dir = f"{os.getcwd()}/{i}"
                    yield i, size_file, file_end, file_dir
            except PermissionError:
                QtWidgets.QMessageBox.information(self, "Ошибка", "У вас недостаточно прав")
            print(self.dir_continue)

    def dir_select(self, select: int = 0):
        if select:
            if os.getcwd() != f"{os.getenv('SystemDrive')}\\":
                self.dir_continue.append(os.getcwd())
                file_dir = os.getcwd().split("\\")
                del file_dir[-1]
                if len(file_dir) == 1:
                    os.chdir(f"{file_dir[0]}\\")
                else:
                    os.chdir("\\".join(file_dir))
        else:
            try:
                os.chdir(self.dir_continue[-1])
                del self.dir_continue[-1]
            except IndexError:
                self.dir_continue.append(os.getcwd())
        self.add_items_table()

    def item_connect(self, item: QtWidgets.QTableWidgetItem):
        if self.indexFromItem(item).column() == 0:
            if self.item(self.indexFromItem(item).row(), 2).text().lower() == "папка":
                os.chdir(self.item(self.indexFromItem(item).row(), 3).text())
                self.add_items_table()
            else:
                os.startfile(item.text())


class Main(QtWidgets.QWidget):
    back_clicked = QtCore.pyqtSignal()
    continue_clicked = QtCore.pyqtSignal()

    def __init__(self):
        super(Main, self).__init__()
        self.resize(700, 400)
        button_back = QtWidgets.QPushButton("Назад")
        button_back.clicked.connect(self.back_clicked.emit)
        button_continue = QtWidgets.QPushButton("Вверх")
        button_continue.clicked.connect(self.continue_clicked.emit)
        self.table = Table(self)
        layout = QtWidgets.QGridLayout()
        layout.addWidget(button_continue, 0, 0)
        layout.addWidget(button_back, 0, 1)
        layout.addWidget(self.table, 1, 0, 1, 2)
        self.setLayout(layout)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main = Main()
    main.show()
    sys.exit(app.exec_())
