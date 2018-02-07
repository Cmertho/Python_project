from PyQt5 import QtWidgets, QtCore, QtGui
import sys
import re
__author__ = "Dmitry Ozolin"


class Time(QtWidgets.QWidget):
    def __init__(self):
        self.seconds, self.minutes, self.hours = "00", "00", "00"
        super().__init__()
        self.setWindowTitle('Таймер обратного отсчета')
        self.resize(400, 400)
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.context)

        self.bar = QtWidgets.QMenuBar()

        open_settings = QtWidgets.QAction('Настройки', self)
        open_settings.triggered.connect(self.setting_dialog)
        open_settings.setShortcut('Alt+F')
        close_file = QtWidgets.QAction('Закрыть программу', self)
        close_file.triggered.connect(lambda: self.close())
        close_file.setShortcut('Alt+Q')
        self.file_menu = self.bar.addMenu('Программа')
        self.file_menu.addAction(open_settings)
        self.file_menu.addSeparator()
        self.file_menu.addAction(close_file)

        self.label_time = QtWidgets.QLabel('До конца осталось 00 : 00 : 00')
        self.label_time.setFont(QtGui.QFont('Arial', font))
        self.button_time = QtWidgets.QPushButton("Задать время таймера")
        self.button_time.clicked.connect(self.setting_dialog)
        self.button_time.setFont(QtGui.QFont('Arial', 15))

        layout_button = QtWidgets.QHBoxLayout()
        self.button_start_time = QtWidgets.QPushButton("Начать отсчет")
        self.button_start_time.setFont(QtGui.QFont('Arial', 15))
        self.button_start_time.setVisible(False)
        self.button_start_time.setShortcut('Alt+S')
        self.button_start_time.clicked.connect(lambda: self.timer.start(1000))

        self.button_stop_time = QtWidgets.QPushButton("Остановить отсчет")
        self.button_stop_time.setFont(QtGui.QFont('Arial', 15))
        self.button_stop_time.setVisible(False)
        self.button_stop_time.setShortcut('Alt+D')
        self.button_stop_time.clicked.connect(lambda: self.timer.stop())
        layout_button.addWidget(self.button_start_time)
        layout_button.addWidget(self.button_stop_time)

        layout_time = QtWidgets.QVBoxLayout()
        layout_time.addWidget(self.label_time, 0, QtCore.Qt.AlignHCenter)
        layout_time.addWidget(self.button_time)
        layout_time.addLayout(layout_button)
        layout_time.setMenuBar(self.bar)
        self.setLayout(layout_time)

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.start_time)

    def setting_dialog(self):
        self.setting = QtWidgets.QDialog()
        self.setting.setWindowTitle('Настройка таймера обратного отсчета')
        self.setting.setFont(QtGui.QFont("Arial", 20))
        hours_layout = QtWidgets.QHBoxLayout()
        label_hours = QtWidgets.QLabel('Количество часов отсчета  ')
        self.edit_hours = QtWidgets.QLineEdit()
        self.edit_hours.setMaxLength(2)
        self.edit_hours.textChanged.connect(self.checked)
        hours_layout.addWidget(label_hours)
        hours_layout.addWidget(self.edit_hours, 0, QtCore.Qt.AlignRight)

        minutes_layout = QtWidgets.QHBoxLayout()
        label_minutes = QtWidgets.QLabel('Количество минут отсчета  ')
        self.edit_minutes = QtWidgets.QLineEdit()
        self.edit_minutes.setMaxLength(2)
        self.edit_minutes.textChanged.connect(self.checked)
        minutes_layout.addWidget(label_minutes)
        minutes_layout.addWidget(self.edit_minutes, 0, QtCore.Qt.AlignRight)

        seconds_layout = QtWidgets.QHBoxLayout()
        label_seconds = QtWidgets.QLabel('Количество секунд отсчета ')
        self.edit_second = QtWidgets.QLineEdit()
        self.edit_second.setMaxLength(2)
        self.edit_second.textChanged.connect(self.checked)
        seconds_layout.addWidget(label_seconds)
        seconds_layout.addWidget(self.edit_second, 0, QtCore.Qt.AlignRight)

        button_save = QtWidgets.QPushButton("Сохранить")
        button_save.clicked.connect(self.setting_save)

        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addLayout(hours_layout)
        main_layout.addLayout(minutes_layout)
        main_layout.addLayout(seconds_layout)
        main_layout.addWidget(button_save)
        self.setting.setLayout(main_layout)
        self.setting.exec()

    def setting_save(self):
        if len(self.edit_hours.text()) == 2:
            self.hours = self.edit_hours.text()
        elif len(self.edit_hours.text()) == 1:
            self.hours = "0%s" % self.edit_hours.text()
        else:
            pass
        if len(self.edit_minutes.text()) == 2:
            self.minutes = self.edit_minutes.text()
        elif len(self.edit_minutes.text()) == 1:
            self.minutes = "0%s" % self.edit_minutes.text()
        else:
            pass

        if len(self.edit_second.text()) == 2:
            self.seconds = self.edit_second.text()
        elif len(self.edit_second.text()) == 1:
            self.seconds = "0%s" % self.edit_second.text()
        else:
            pass
        self.label_time.setText('До конца осталось %s : %s : %s' % (self.hours, self.minutes, self.seconds))

        self.setting.close()
        self.button_time.setVisible(False)
        self.button_stop_time.setVisible(True)
        self.button_start_time.setVisible(True)

    def checked(self, time):
        time = check.sub("", time)
        if self.edit_hours.isModified():
            self.edit_hours.setText(time)
        if self.edit_minutes.isModified():
            self.edit_minutes.setText(time)
        if self.edit_second.isModified():
            self.edit_second.setText(time)

    def start_time(self):
        if int(self.seconds) == 0:
            self.seconds = 59
            self.minutes = int(self.minutes) - 1
            if len(str(self.minutes)) == 1:
                self.minutes = "0%s" % self.minutes
            self.label_time.setText('До конца осталось %s : %s : %s' % (self.hours, self.minutes, self.seconds))
        else:
            self.seconds = int(self.seconds) - 1
            if len(str(self.seconds)) == 1:
                self.seconds = "0%s" % self.seconds
                self.label_time.setText('До конца осталось %s : %s : %s' % (self.hours, self.minutes, self.seconds))
            else:
                self.label_time.setText('До конца осталось %s : %s : %s' % (self.hours, self.minutes, self.seconds))
        if int(self.minutes) <= 0:
            self.minutes = 59
            self.hours = int(self.hours) - 1
            if len(str(self.hours)) == 1:
                self.hours = "0%s" % self.hours
            self.label_time.setText('До конца осталось %s : %s : %s' % (self.hours, self.minutes, self.seconds))
        if int(self.hours) == -1:
            self.seconds, self.minutes, self.hours = "00", "00", "00"
            self.label_time.setText('До конца осталось 00 : 00 : 00')
            self.button_time.setVisible(True)
            self.button_stop_time.setVisible(False)
            self.button_start_time.setVisible(False)
            self.timer.stop()

    def context(self, point):
        def visible():
                self.button_start_time.setVisible(False)
                self.button_stop_time.setVisible(False)
                self.bar.setVisible(False)
                self.button_time.setVisible(False)

        def visible_true():
                self.button_start_time.setVisible(True)
                self.button_stop_time.setVisible(True)
                self.bar.setVisible(True)
                self.button_time.setVisible(False)

        menu_context = QtWidgets.QMenu()
        self.visible_widget = QtWidgets.QAction('Скрыть виджеты')
        self.visible_widget.triggered.connect(visible)
        self.visible_widget.setShortcut('Alt+V')
        self.visible_widget_false = QtWidgets.QAction('Раскрыть виджеты')
        self.visible_widget_false.triggered.connect(visible_true)
        self.visible_widget_false.setShortcut('Alt+V')
        menu_context.addAction(self.visible_widget)
        menu_context.addAction(self.visible_widget_false)
        menu_context.addSeparator()
        menu_family = menu_context.addMenu('Шрифты')
        new_roman = QtWidgets.QAction('Шрифт Times New Roman')
        new_roman.setFont(QtGui.QFont('Times New Roman'))
        new_roman.triggered.connect(lambda: self.label_time.setFont(QtGui.QFont('Times New Roman', font)))

        arial = QtWidgets.QAction('Шрифт Arial')
        arial.setFont(QtGui.QFont('Arial'))
        arial.triggered.connect(lambda: self.label_time.setFont(QtGui.QFont('Arial', font)))

        georgia = QtWidgets.QAction('Шрифт Georgia')
        georgia.setFont(QtGui.QFont('Georgia'))
        georgia.triggered.connect(lambda: self.label_time.setFont(QtGui.QFont('Georgia', font)))

        menu_family.addAction(arial)
        menu_family.addAction(new_roman)
        menu_family.addAction(georgia)

        menu_context.exec(self.mapToGlobal(point))


if __name__ == "__main__":
    font = 50
    check = re.compile('[^\W(0-9)]')
    app = QtWidgets.QApplication(sys.argv)
    main = Time()
    main.show()
    sys.exit(app.exec_())
