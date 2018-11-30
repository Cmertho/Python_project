import sys
import sqlite3
import json
from PyQt5 import QtWidgets, QtGui, QtCore


def log_uncaught_exceptions(ex_cls, ex, tb):
    text = '{}: {}:\n'.format(ex_cls.__name__, ex)
    import traceback
    text += ''.join(traceback.format_tb(tb))

    print(text)
    sys.exit(1)


sys.excepthook = log_uncaught_exceptions


class Main(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.timer = Timer(self)
        self.setStyleSheet("""
            QMainWindow{
                background: #fff;
            }
            QPushButton{
                background: #fff;
                border: 0px;
            }
        """)
        self.setCentralWidget(self.timer)

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.old_pos = None

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.old_pos = event.pos()

    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.old_pos = None

    def mouseMoveEvent(self, event):
        if not self.old_pos:
            return
        delta = event.pos() - self.old_pos
        self.move(self.pos() + delta)

    def setFixedSize(self, size: list):
        if isinstance(size, list) or isinstance(size[0], int):
            super().setFixedSize(*size)
        else:
            x_size, y_size = size.split("x")
            super().setFixedSize(int(x_size), int(y_size))


class Timer(QtWidgets.QWidget):
    def __init__(self, parent: Main = None):
        super().__init__(parent)
        self.main = parent
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.context)
        self.menu = QtWidgets.QMenuBar()
        menu_file = self.menu.addMenu("Приложение")
        setting_event = menu_file.addAction("Настройки приложения")
        setting_event.triggered.connect(self.open_dialog)
        setting_event.setShortcut("Alt+W")

        font_event = menu_file.addAction("Настройки текста")
        font_event.triggered.connect(self.update_text_font)
        font_event.setShortcut('Alt+E')
        close_event = menu_file.addAction("Закрыть приложение")
        close_event.setShortcut('Alt+Q')
        close_event.triggered.connect(lambda: sys.exit(1))

        windows_size = self.menu.addMenu("Расширение приложение")
        size_640_480 = windows_size.addAction("640x480")
        size_640_480.triggered.connect(lambda: self.custom_size(0, 640, 480))
        size_800_600 = windows_size.addAction("800x600")
        size_800_600.triggered.connect(lambda: self.custom_size(0, 800, 600))
        size_1024_768 = windows_size.addAction("1024x768")
        size_1024_768.triggered.connect(lambda: self.custom_size(0, 1024, 768))
        size_any = windows_size.addAction("Кастомное расширение")
        size_any.triggered.connect(lambda: self.custom_size(1))

        with open("setting.json", encoding="utf-8") as file:
            settings = json.loads(file.read())
        self.main.setFixedSize(settings["size"])
        self.seconds, self.minutes,  self.hours = 0, 0, 2
        self.label = QtWidgets.QLabel("Информационная безопасность")
        self.label.setFont(QtGui.QFont(*settings["label"]))
        self.timer = QtWidgets.QLabel("%02d : %02d : %02d" % (self.hours, self.minutes, self.seconds))
        self.timer.setFont(QtGui.QFont(*settings["times"]))

        self.button_start = QtWidgets.QPushButton("Начать отсчет")
        self.button_start.setShortcut('Alt+S')
        self.button_start.clicked.connect(lambda: self.timer_tick.start(1000))
        self.button_start.setFont(QtGui.QFont(*settings["button"]))
        self.button_stop = QtWidgets.QPushButton("Закончить отсчет")
        self.button_stop.setFont(QtGui.QFont(*settings["button"]))
        self.button_stop.clicked.connect(lambda: self.timer_tick.stop())
        self.button_stop.setShortcut('Alt+D')

        self.image_parent = QtGui.QPixmap()
        self.image = QtWidgets.QLabel()
        self.image.setScaledContents(True)

        layout = QtWidgets.QGridLayout()
        layout.addWidget(self.image, 0, 0, 1, 2, QtCore.Qt.AlignCenter)
        layout.addWidget(self.label, 1, 0, 1, 2, QtCore.Qt.AlignCenter)
        layout.addWidget(self.timer, 2, 0, 1, 2, QtCore.Qt.AlignCenter)
        layout.addWidget(self.button_start, 3, 0)
        layout.addWidget(self.button_stop, 3, 1)
        layout.setMenuBar(self.menu)
        self.setLayout(layout)
        self.base()
        self.timer_tick = QtCore.QTimer()
        self.timer_tick.timeout.connect(self.start_time)

    def base(self):
        conn = sqlite3.connect("saves.db")
        con = conn.cursor()
        executes = con.execute("select Image, Text from Times where ID like 1")
        image, text = executes.fetchone()
        self.image_parent.loadFromData(image)
        self.image.setPixmap(self.image_parent)
        self.label.setText(text)

    @staticmethod
    def save_image(image):
        with open(image, "rb") as file_image, sqlite3.connect("saves.db") as conn:
            conn.execute("update Times set Image=? where ID = 1", (file_image.read(),))

    def start_time(self):

        if self.seconds == 0:
            if self.minutes == 0:
                if self.hours == 0:
                    self.timer.setText('СТОП!')
                    self.timer_tick.stop()
                else:
                    self.hours -= 1
                    self.minutes = 59
                    self.seconds = 59
            else:
                self.minutes -= 1
                self.seconds = 59
        else:
            self.seconds -= 1
        if self.timer.text() == "СТОП!":
            pass
        else:
            self.timer.setText('%02d : %02d : %02d' % (self.hours, self.minutes, self.seconds))

    def open_dialog(self):
        self.dialog = SettingDialog(self, str(self.hours), str(self.minutes), str(self.seconds), self.label.text())
        self.dialog.exec_()

    def context(self, point):
        menu = QtWidgets.QMenu()
        event_close = QtWidgets.QAction("Убарть кнопки / Добавить кнопки")
        event_close.triggered.connect(self.event_del)
        event_image_close = QtWidgets.QAction("Деофлное изображение / подстроить под приложение изображение")
        event_image_close.triggered.connect(self.image_resize)
        menu.addAction(event_close)
        menu.addAction(event_image_close)
        menu.exec_(self.mapToGlobal(point))

    def event_del(self):
        if self.button_start.isVisible():
            self.button_start.setVisible(False)
            self.button_stop.setVisible(False)
            self.menu.setVisible(False)
        else:
            self.button_start.setVisible(True)
            self.button_stop.setVisible(True)
            self.menu.setVisible(True)

    def image_resize(self):
        if self.image.hasScaledContents():
            self.image.setScaledContents(False)
        else:
            self.image.setScaledContents(True)

    def update_text_font(self):
        self.font_style = FontChange(self)
        self.font_style.exec_()

    def custom_size(self, t: int, size_x: int = None, size_y: int = None):
        def save():
            if all([line_x.text(), line_y.text()]):
                with open("setting.json", encoding="utf-8") as file_1:
                    settings = json.loads(file_1.read())
                    settings["size"] = [int(line_x.text()), int(line_y.text())]
                    self.main.setFixedSize(settings["size"])
                with open("setting.json", "w", encoding="utf-8") as file_write_1:
                    file_write_1.write(json.dumps(settings, ensure_ascii=False, indent=4))
            self.size_custom.close()

        if t == 1:
            self.size_custom = QtWidgets.QDialog()
            self.size_custom.setWindowTitle("Настройка")
            self.size_custom.setStyleSheet("""
                QLineEdit, QLabel, QPushButton{
                    font: 20px Time New Roman;
                }
            """)
            self.size_custom.setWindowFlags(QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint)
            line_x = QtWidgets.QLineEdit()
            line_y = QtWidgets.QLineEdit()
            button = QtWidgets.QPushButton("Сохранить")
            button.clicked.connect(save)
            layout = QtWidgets.QGridLayout()
            layout.addWidget(line_x, 0, 0)
            layout.addWidget(QtWidgets.QLabel("x"), 0, 1)
            layout.addWidget(line_y, 0, 2)
            layout.addWidget(button, 1, 0, 1, 3)
            self.size_custom.setLayout(layout)
            self.size_custom.exec_()
        else:
            with open("setting.json", encoding="utf-8") as file:
                settings_1 = json.loads(file.read())
                settings_1["size"] = [size_x, size_y]
                self.main.setFixedSize(settings_1["size"])
            with open("setting.json", "w", encoding="utf-8") as file_write:
                file_write.write(json.dumps(settings_1, ensure_ascii=False, indent=4))


class SettingDialog(QtWidgets.QDialog):
    def __init__(self, parent: Timer = None, hours: str = None, minutes: str = None, seconds: str = None,
                 title: str = None):
        super().__init__()
        self.setWindowTitle("Настройки")
        self.setWindowFlags(QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint)
        self.setStyleSheet("""
            QDialog{
                background: #fff;
            }
            QPushButton{
                font: 20px Times New Roman italic;
                border: 0px;
            }
            QPushButton:hover{
                border:  1px double #05f;
            }
            QLabel, QLineEdit{
                font: 20px Times New Roman italic;
            }
        """)
        self.root = parent
        if self.root.timer_tick.isActive():
            self.root.timer_tick.stop()
        self.button_save = QtWidgets.QPushButton("Сохранить изменения")
        self.button_image = QtWidgets.QPushButton("Добавить / Изменить изображение")
        self.button_image.clicked.connect(self.add_image)
        self.button_save.clicked.connect(self.save)
        self.button_image_delete = QtWidgets.QPushButton("Удалить изображение")
        self.button_image_delete.clicked.connect(self.delete_image)
        self.seconds, self.minutes, self.hours = QtWidgets.QLineEdit(), QtWidgets.QLineEdit(), QtWidgets.QLineEdit()
        self.seconds.setText(seconds)
        self.minutes.setText(minutes)
        self.hours.setText(hours)
        self.seconds.setValidator(QtGui.QIntValidator(0, 60))
        self.minutes.setValidator(QtGui.QIntValidator(0, 60))
        self.line_text = QtWidgets.QLineEdit()
        self.line_text.setText(title)
        layout = QtWidgets.QGridLayout()
        layout.addWidget(QtWidgets.QLabel("Название компитенции"), 0, 0, 1, 3, QtCore.Qt.AlignCenter)
        layout.addWidget(self.line_text, 1, 0, 1, 3)
        layout.addWidget(QtWidgets.QLabel("Часы"), 2, 0, QtCore.Qt.AlignCenter)
        layout.addWidget(QtWidgets.QLabel("Минуты"), 2, 1, QtCore.Qt.AlignCenter)
        layout.addWidget(QtWidgets.QLabel("Секунды"), 2, 2, QtCore.Qt.AlignCenter)
        layout.addWidget(self.hours, 3, 0)
        layout.addWidget(self.minutes, 3, 1)
        layout.addWidget(self.seconds, 3, 2)
        layout.addWidget(self.button_save, 4, 0, 1, 3)
        layout.addWidget(self.button_image, 5, 0, 1, 3)
        layout.addWidget(self.button_image_delete, 6, 0, 1, 3)
        layout.addWidget(self.button_save, 7, 0, 1, 3)
        self.setLayout(layout)

    def save(self):
        hours, minutes, seconds = self.hours.text(), self.minutes.text(), self.seconds.text()
        if not hours:
            hours = 0
        if not minutes:
            minutes = 0
        if not seconds:
            seconds = 0
        if self.line_text.text() != self.root.label.text():
            with sqlite3.connect("saves.db") as file:
                file.execute("update Times set Text=? where ID = 1", (self.line_text.text(),))
            self.root.label.setText(self.line_text.text())

        self.root.hours = int(hours)
        self.root.minutes = int(minutes)
        self.root.seconds = int(seconds)
        self.root.timer.setText("%02d : %02d : %02d" % (self.root.hours, self.root.minutes, self.root.seconds))
        self.close()

    def delete_image(self):
        self.root.image.clear()

    def add_image(self):
        file = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', ' ', "*jpg *png *bmp *jpeg *gif")[0]
        if file:
            self.pix = QtGui.QPixmap(file)
            self.root.image.setPixmap(self.pix)
            self.root.save_image(file)


class FontChange(QtWidgets.QDialog):
    def __init__(self, parent: Timer = None):
        super().__init__()
        self.main = parent
        self.setWindowTitle("Настройки")
        self.setWindowFlags(QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint)
        self.setStyleSheet("""
            QLabel, QPushButton{
                font: 20px Times New Roman;
            }
        """)
        with open("setting.json", encoding="utf-8") as file:
            self.setting = json.loads(file.read())
        self.label_text_title = QtWidgets.QLabel("Размер и тип шрифта для названия компитенции\n{} {}".format(
            self.setting["label"][0], self.setting["label"][1]))
        self.label_time = QtWidgets.QLabel("Размер и тип шрифта для таймера\n{} {}".format(
            self.setting["times"][0], self.setting["times"][1]))
        self.label_button = QtWidgets.QLabel("Размер и тип шрифта для кнопок\n{} {}".format(
            self.setting["button"][0], self.setting["button"][1]))

        button_text_title = QtWidgets.QPushButton("Выбрать другой шрифт/размер")
        button_text_title.clicked.connect(lambda: self.update_text(1))
        button_time = QtWidgets.QPushButton("Выбрать другой шрифт/размер")
        button_time.clicked.connect(lambda: self.update_text(2))
        button_size = QtWidgets.QPushButton("Выбрать другой шрифт/размер")
        button_size.clicked.connect(lambda: self.update_text(3))
        layout = QtWidgets.QFormLayout()
        layout.addRow(self.label_text_title, button_text_title)
        layout.addRow(self.label_time, button_time)
        layout.addRow(self.label_button, button_size)
        self.setLayout(layout)

    def update_text(self, type_button: int = None):
        font, ok = QtWidgets.QFontDialog.getFont()
        if ok:
            font_get = font.toString().split(",")[:2]
            font_get[1] = int(font_get[1])
            if type_button == 1:
                self.main.label.setFont(font)
                self.setting["label"] = font_get
            elif type_button == 2:
                self.main.timer.setFont(font)
                self.setting["times"] = font_get
            elif type_button == 3:
                self.main.button_stop.setFont(font)
                self.main.button_start.setFont(font)
                self.setting["button"] = font_get
            with open("setting.json", "w", encoding="utf-8") as file:
                file.write(json.dumps(self.setting, ensure_ascii=False, indent=4))
        self.label_button.setText("Размер и тип шрифта для кнопок\n{} {}".format(
            self.setting["button"][0], self.setting["button"][1]))
        self.label_text_title.setText("Размер и тип шрифта для названия компитенции\n{} {}".format(
            self.setting["label"][0], self.setting["label"][1]))
        self.label_time.setText("Размер и тип шрифта для таймера\n{} {}".format(
            self.setting["times"][0], self.setting["times"][1]))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main = Main()
    main.show()
    sys.exit(app.exec_())
