import sys
import configparser
import re
import random
import transliterate
from PyQt5 import QtCore, QtWidgets, QtGui
import pymysql

# encoding: utf-8
__version__ = 0.3
__author__ = 'Twiss'


class AuthenticationProfile(QtWidgets.QFrame):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Profile Authentication')
        self.setFixedSize(500, 300)
        self.setFont(QtGui.QFont('Times New Roman', 13))
        self.label = QtWidgets.QLabel('Введите ваш логин и пароль', self)
        self.text_login = QtWidgets.QLineEdit(self)
        self.text_login.setPlaceholderText('Введите сюда свой логин')
        self.text_login.setMaxLength(30)
        self.text_login.setEchoMode(0)
        self.text_login.setToolTip('Максимум 30 значений')
        self.text_password = QtWidgets.QLineEdit(self)
        self.text_password.setEchoMode(2)
        self.text_password.setPlaceholderText('Введите сюда свой пароль')
        self.text_password.setMaxLength(30)
        self.text_password.setToolTip('Максимум 30 значений')
        self.accept_button = QtWidgets.QPushButton('Авторизоваться')
        self.accept_button.clicked.connect(self.open_file)
        self.surname = QtWidgets.QLineEdit(self)
        self.surname.setPlaceholderText('Введите сюда вашу ФИО')
        self.surname.setMaxLength(50)
        self.surname.setToolTip('Максимум 30 значений')
        self.combo = QtWidgets.QComboBox()
        self.combo.addItems(["Не выбрано", "9-ПКС", '9-КСК', "9-ПБ", "9-ИБ", "9-C"])
        self.registry_button = QtWidgets.QPushButton('Регистрация')
        self.registry_button.clicked.connect(self.registry_file)
        self.registry_button_accept = QtWidgets.QPushButton('Зарегестрироваться')
        self.registry_button_accept.clicked.connect(self.checked_text)

        self.dictionary_authentication = {"authentication": [self.accept_button, self.text_password,
                                                             self.text_login, self.label],
                                          "registry": [self.surname, self.combo, self.registry_button_accept]}

        self.layout_authentication = QtWidgets.QVBoxLayout()
        self.layout_authentication.addWidget(self.label, 0, QtCore.Qt.AlignCenter)
        self.layout_authentication.addWidget(self.surname)
        self.layout_authentication.addWidget(self.text_login)
        self.layout_authentication.addWidget(self.text_password)
        self.layout_authentication.addWidget(self.combo)
        for items in self.dictionary_authentication["registry"]:
            items.setVisible(False)
        self.vertical_layout = QtWidgets.QHBoxLayout()
        self.vertical_layout.addWidget(self.accept_button)
        self.vertical_layout.addWidget(self.registry_button)
        self.vertical_layout.addWidget(self.registry_button_accept)
        self.layout_authentication.addLayout(self.vertical_layout)
        self.setLayout(self.layout_authentication)

    def open_file(self):
        # функция содержит в себе ошибку при неудачной аутентификации, а так же перенаправления в "кэш" логин и пароль.
        # Сначало будет проверяться база данных которая будет храниться у пользователя если там не будет данных, то она
        # будет выдавать исключение т.е. поиск уже по базе MySQL, а если уже и там не будет то предоставит регистрацию.
        reply = QtWidgets.QMessageBox(self)
        reply.setFont(QtGui.QFont('Times New Roman', 13))
        reply.setIcon(QtWidgets.QMessageBox.Critical)
        reply.setWindowTitle("Аудентификация")
        try:
            surname = DataBase.connect_to_data_base(self.text_login.text(), self.text_password.text())
            if surname:
                for sur in surname:
                    profile_name.clear()
                    profile_name.append(sur[0])
                    profile_name.append(sur[1])
                    profile_name.append(sur[2])
                    profile_name.append(sur[3])
                    profile_name.append("admin_base")
                    self.main = MainWindows()
                    try:
                        self.main.show()
                        self.close()
                    except IndexError:
                        self.main.show()
                        self.close()
                    except pymysql.ProgrammingError as error:
                        if error.args == (1064, "You have an error in your SQL syntax; check the manual that "
                                                "corresponds to your MySQL server version for the right syntax "
                                                "to use near '' at line 1"):
                            self.main.show()
                            self.close()
            else:
                reply.setText('Не верный логин / пароль')
                reply.show()
                self.text_password.clear()

        except pymysql.OperationalError as e:
            if e.args == (2003, "Can't connect to MySQL server on 'dmozolin.mix-studio.ru' "
                                "([Errno 11001] getaddrinfo failed)"):
                reply.setText("Нет доступа к интернету")
                reply.show()
            else:
                reply.setText("Нет доступа к серверу обратитесь к администратору код ошибки" + '\n' + str(e.args))
                reply.show()

    def registry_file(self):
        self.accept_button.setVisible(False)
        self.registry_button.setVisible(False)
        for visible_button_true in self.dictionary_authentication["registry"]:
            visible_button_true.setVisible(True)
        self.label.setText('Заполните все поля')

    def checked_text(self):
        if not (self.text_login.text() and self.text_login.text().strip()):
            self.text_login.setToolTip('<h2>Заполните поле логина</h2>')
            return QtCore.QTimer.singleShot(1, lambda: QtWidgets.QToolTip.showText(
                self.mapToGlobal(self.text_login.pos()), self.text_login.toolTip(),
                self.text_login, QtCore.QRect()))
        if not (self.text_password.text() and self.text_password.text().strip()):
            self.text_password.setToolTip('<h2>Заполните поле пароля</h2>')
            return QtCore.QTimer.singleShot(1, lambda: QtWidgets.QToolTip.showText(
                self.mapToGlobal(self.text_password.pos()), self.text_password.toolTip(),
                self.text_password, QtCore.QRect()))
        if not (self.surname.text() and self.surname.text().strip()):
            self.surname.setToolTip('<h2>Заполните поле ФИО</h2>')
            return QtCore.QTimer.singleShot(1, lambda: QtWidgets.QToolTip.showText(
                self.mapToGlobal(self.surname.pos()), self.surname.toolTip(),
                self.surname, QtCore.QRect()))
        if self.combo.currentText() == "Не выбрано":
            reply = QtWidgets.QMessageBox(self)
            reply.setFont(QtGui.QFont('Times New Roman', 13))
            reply.setIcon(QtWidgets.QMessageBox.Critical)
            reply.setWindowTitle("Выбирете группу")
            reply.setText('Выбирете группу в которой вы учитесь')
            return reply.exec()
        self.registry(self.text_login.text())

    def registry(self, text):
        reply = QtWidgets.QMessageBox(self)
        reply.setFont(QtGui.QFont('Times New Roman', 13))
        reply.setIcon(QtWidgets.QMessageBox.Critical)
        reply.setWindowTitle("Критическая ошибка")
        try:
            data_base_name = transliterate.translit(text, reversed=True)
            data_base_name = blank_name.sub('', data_base_name)
        except transliterate.exceptions.LanguageDetectionError:
            data_base_name = blank_name.sub('', text)
        try:
            with pymysql.connect(host=host,
                                 port=3306,
                                 user=user,
                                 password=password,
                                 db="test_create",
                                 charset='utf8') as cur:
                # Создание базы для преподавателей
                    '''cur.execute("CREATE TABLE %s "
                                "(ID INTEGER PRIMARY KEY NOT NULL AUTO_INCREMENT, "
                                "real_name_test CHAR ( 50 ),"
                                "availability CHAR( 50))" % data_base_name) '''
                    cur.execute("INSERT INTO authentication (ID, Login, Password, Surname, Position, Groups, "
                                "name_table) VALUE(NULL, %s, %s, %s, %s, %s, %s)",
                                (self.text_login.text(), self.text_password.text(), self.surname.text(), "Студент",
                                 self.combo.currentText(), data_base_name))
                    cur.close()
                    self.label.setText('Введите логин или пароль')
                    for item_true in self.dictionary_authentication["authentication"]:
                        item_true.setVisible(True)
                    for item_false in self.dictionary_authentication["registry"]:
                        item_false.setVisible(False)
        except pymysql.err.InternalError:
            reply.setText("Пользователь с данным логином уже существует ")
            reply.show()
        except pymysql.err.OperationalError as e:
            if e.args == (2003, "Can't connect to MySQL server on 'dmozolin.mix-studio.ru' "
                                "([Errno 11001] getaddrinfo failed)"):
                reply.setText("Нет доступа к интернету")
                reply.show()
            else:
                reply.setText("Нет доступа к серверу обратитесь к администратору код ошибки" + '\n' + str(e.args))
                reply.show()
        except pymysql.err.ProgrammingError:
            return


class RightFrame(QtWidgets.QFrame):
    def __init__(self, main, **kwargs):
        super().__init__(main, **kwargs)
        self.mains = main
        self.setFrameShape(QtWidgets.QFrame.StyledPanel)
        box_right = QtWidgets.QHBoxLayout()

        self.label_choice = QtWidgets.QLabel(self)
        self.label_choice.setText('Для начала работы нажмите на любой тест')
        self.label_choice.setFont(QtGui.QFont('Times New Roman', 15))
        self.label_choice.setVisible(True)

        self.choice_questions = QtWidgets.QTreeWidget(self)
        self.choice_questions.setFixedSize(850, 400)
        self.choice_questions.setHeaderLabels(
            ["№", "Вопрос", "Ответ №1", "Ответ №2", "Ответ №3", "Ответ №4", "Ответ №5", "Правильный ответ"])
        self.choice_questions.setFont(QtGui.QFont('Times New Roman', 13))
        self.choice_questions.setVisible(False)
        self.choice_questions.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.choice_questions.customContextMenuRequested.connect(self.select_items_data_base)

        self.button_start = QtWidgets.QCommandLinkButton("Начать тест", self)
        self.button_start.clicked.connect(self.open_test)
        self.button_start.setVisible(False)

        box_right.addWidget(self.label_choice, 0, QtCore.Qt.AlignCenter)
        if profile_name[1] == 'Преподаватель':

            box_right.addWidget(self.choice_questions, 0, QtCore.Qt.AlignBottom | QtCore.Qt.AlignRight)
        else:

            box_right.addWidget(self.button_start, 0, QtCore.Qt.AlignBottom | QtCore.Qt.AlignRight)
        self.setLayout(box_right)

    def add_question_list_widget(self, items):
        # вывод данных из выбраной пользователем базы данных
        self.item = items
        self.label_choice.setVisible(False)
        # Следующая строка будет включать в себя базу данных вопросов на тесты
        # items - ведет поиск по всем вопросам которые находятся в бд предмета который использует пользователь
        self.choice_questions.clear()
        self.choice_questions.setVisible(True)
        for item in range(len(self.item)):
            tree_caption = QtWidgets.QTreeWidgetItem([str(item + 1), str(self.item[item][0]),
                                                      str(self.item[item][1]), str(self.item[item][2]),
                                                      str(self.item[item][3]), str(self.item[item][4]),
                                                      str(self.item[item][5]),
                                                      str(blank_name.sub('', self.item[item][6]))])
            self.choice_questions.addTopLevelItem(tree_caption)

    def select_items_data_base(self, point):
        menu = QtWidgets.QMenu()
        if self.choice_questions.itemAt(point):
            edit_question = QtWidgets.QAction('Редактировать вопрос', menu)
            edit_question.triggered.connect(lambda: self.select_edit_question(point))
            menu.addAction(edit_question)
            # menu.addSeparator()
            delete_question = QtWidgets.QAction('Удалить вопрос', menu)
            delete_question.triggered.connect(lambda: DataBase.delete_question(self.choice_questions.
                                                                               itemAt(point).text(1)))
            delete_question.triggered.connect(lambda: self.mains.test_list_widget(profile_name[4]))
            menu.addAction(delete_question)
        else:
            create_test_radio = QtWidgets.QAction('Создать вопрос с одним вариантом ответов', menu)
            create_test_radio.triggered.connect(lambda: self.mains.radio_box_create.value_checked(1))
            menu.addAction(create_test_radio)
            menu.addSeparator()
            create_test_check = QtWidgets.QAction('Создать вопрос с несколькими вариантами ответа', menu)
            create_test_check.triggered.connect(lambda: self.mains.radio_box_create.value_checked(2))
            menu.addAction(create_test_check)
        menu.exec(self.choice_questions.mapToGlobal(point))

    def select_edit_question(self, index_id):
        text = []
        for item in range(self.choice_questions.itemAt(index_id).columnCount()):
            text.append(self.choice_questions.itemAt(index_id).text(item))
        print(text)
        self.dialog_edit_question = QtWidgets.QDialog()
        self.dialog_edit_question.entry = QtWidgets.QLabel()

    def open_test(self):
        self.test_students = StudentTest()
        self.test_students.show()


class LeftFrame(QtWidgets.QFrame):
    def __init__(self, main, **kwargs):
        super().__init__(main, **kwargs)
        self.mains = main
        self.context = AuthenticationProfile()
        self.setMaximumWidth(300 - x_global_range)
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.context_menu_label_left_frame)
        self.choice_tests = QtWidgets.QListWidget(self)
        self.choice_tests.setFont(QtGui.QFont('Times New Roman', 13))
        self.choice_tests.setSpacing(4)
        self.choice_tests.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        for i in DataBase.add_to_list_question():
            self.choice_tests.addItems([str(*i)])

        self.label = QtWidgets.QLabel(self)
        self.label.setText(profile_name[0])

        layout_left_frame = QtWidgets.QVBoxLayout()
        layout_left_frame.addWidget(self.label, 0, QtCore.Qt.AlignCenter)
        layout_left_frame.addWidget(self.choice_tests, QtCore.Qt.AlignCenter)
        self.setLayout(layout_left_frame)

        if profile_name[1] == 'Преподаватель':
            self.choice_tests.customContextMenuRequested.connect(self.context_menu_test_left_frame)
            self.choice_tests.itemDoubleClicked.connect(main.test_list_widget)

        elif profile_name[1] == 'Студент':
            self.choice_tests.itemDoubleClicked.connect(main.open_about)

    def context_menu_test_left_frame(self, point):
        menu = QtWidgets.QMenu()
        if self.choice_tests.itemAt(point):
            edit_test = QtWidgets.QAction('Редактировать тест', menu)
            edit_test.triggered.connect(lambda: self.edit_test_profile(point))
            menu.addAction(edit_test)
            menu.addSeparator()
            delete_test = QtWidgets.QAction('Удалить тест', menu)
            delete_test.triggered.connect(lambda: self.delete_test_profile(point))
            menu.addAction(delete_test)
        else:
            create_db = QtWidgets.QAction('Создать новый тест', menu)
            create_db.triggered.connect(self.table_add_to_database)
            menu.addAction(create_db)
            menu.addSeparator()
            quit_user = QtWidgets.QAction('Выйти из профиля', menu)
            quit_user.triggered.connect(self.mains.close)
            quit_user.triggered.connect(lambda: self.context.show())
            menu.addAction(quit_user)
        menu.exec(self.choice_tests.mapToGlobal(point))

    def context_menu_label_left_frame(self, point):
        menu = QtWidgets.QMenu()
        open_profile = QtWidgets.QAction('Открыть профиль', menu)
        open_profile.triggered.connect(self.open_profile)
        menu.addAction(open_profile)
        menu.addSeparator()
        quit_profile = QtWidgets.QAction('Выйти из профиля', menu)
        quit_profile.triggered.connect(self.mains.close)
        quit_profile.triggered.connect(lambda: self.context.show())
        menu.addAction(quit_profile)
        menu.exec(self.mapToGlobal(point))

    def delete_test_profile(self, points):
        def check_button_delete_test(id_name):
            # удаление таблицы из бд нужно окно предпупреждения P.S. Добавить само удаление из базы данных
            if button_group.id(id_name) == 1:
                DataBase.delete_test(self.choice_tests.itemAt(points).text())
                self.choice_tests.takeItem(self.choice_tests.row(self.choice_tests.itemAt(points)))
                self.mains.right.choice_questions.setVisible(False)
                reply.close()
            elif button_group.id(id_name) == 2:
                reply.close()

        def tick():
            if self.tick_seconds:
                self.tick_seconds -= 1
                button_yes.setText("Да ({})".format(self.tick_seconds))
            else:
                timer.stop()
                button_yes.setText("Да")
                button_yes.setEnabled(True)

        self.tick_seconds = 5
        reply = QtWidgets.QDialog()
        reply.setFont(QtGui.QFont('Times New Roman', 13))
        v_box = QtWidgets.QVBoxLayout()
        label_dialog = QtWidgets.QLabel('Вы действительно хотите удалить {} ?'
                                        .format(self.choice_tests.itemAt(points).text()))
        button_no = QtWidgets.QPushButton('Нет', reply)
        button_yes = QtWidgets.QPushButton("Да (5)", reply)
        button_yes.setEnabled(False)
        button_group = QtWidgets.QButtonGroup()
        button_group.addButton(button_yes, 1)
        button_group.addButton(button_no, 2)
        button_group.buttonClicked.connect(check_button_delete_test)
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(button_yes)
        layout.addWidget(button_no)
        v_box.addWidget(label_dialog)
        v_box.addSpacing(20)
        v_box.addLayout(layout)
        reply.setLayout(v_box)
        timer = QtCore.QTimer()
        timer.timeout.connect(tick)
        timer.start(1000)
        reply.exec()

    def open_profile(self):
        # Открытие карточки пользователя где содержиться информация
        self.dialog_profile_test = QtWidgets.QDialog()
        self.dialog_profile_test.setFont(QtGui.QFont(configuration_text[0], configuration_text[1]))
        layout_vertical = QtWidgets.QVBoxLayout()
        self.dialog_profile_test.resize(600, 400)
        self.dialog_profile_test.setWindowTitle('Профиль ' + profile_name[0])
        self.dialog_profile_test.label_name = QtWidgets.QLabel()
        self.dialog_profile_test.label_name.setText('Карточка Пользователя')

        layout_horizontal_name = QtWidgets.QHBoxLayout()
        self.dialog_profile_test.label_fio = QtWidgets.QLabel("ФИО")

        self.dialog_profile_test.edit_login = QtWidgets.QLineEdit()
        self.dialog_profile_test.edit_login.setPlaceholderText(profile_name[0])
        self.dialog_profile_test.edit_login.setMaxLength(30)
        self.dialog_profile_test.edit_login.textEdited.connect(self.check_login_text)

        layout_horizontal_name.addWidget(self.dialog_profile_test.label_fio)
        layout_horizontal_name.addWidget(self.dialog_profile_test.edit_login)

        self.dialog_profile_test.label_position = QtWidgets.QLabel()
        self.dialog_profile_test.label_position.setText('Должность     ' + profile_name[1])

        self.dialog_profile_test.label_group = QtWidgets.QLabel()
        self.dialog_profile_test.label_group.setText('Группа           ' + profile_name[2])
        self.dialog_profile_test.label_group.setVisible(False)

        self.dialog_profile_test.accept_button = QtWidgets.QPushButton()
        self.dialog_profile_test.accept_button.setText('Выйти')
        self.dialog_profile_test.accept_button.clicked.connect(self.enter_login_db)

        if "Студент" in self.dialog_profile_test.label_position.text():
            self.dialog_profile_test.label_group.setVisible(True)

        layout_vertical.addWidget(self.dialog_profile_test.label_name, 0, QtCore.Qt.AlignCenter)
        layout_vertical.addLayout(layout_horizontal_name)
        layout_vertical.addWidget(self.dialog_profile_test.label_position)
        layout_vertical.addWidget(self.dialog_profile_test.label_group)
        layout_vertical.addWidget(self.dialog_profile_test.accept_button)

        self.dialog_profile_test.setLayout(layout_vertical)

        self.dialog_profile_test.exec()

    def check_login_text(self):
        if re.compile("[^a-zA-Z,а-яА-я]").sub('', self.dialog_profile_test.edit_login.text()):
            self.dialog_profile_test.accept_button.setText('Изменить')
        else:
            self.dialog_profile_test.accept_button.setText('Выйти')

    def enter_login_db(self):
        if self.dialog_profile_test.accept_button.text() == 'Изменить':
            self.label.setText(self.dialog_profile_test.edit_login.text())
            self.dialog_profile_test.close()
        else:
            self.dialog_profile_test.close()

    def table_add_to_database(self):
        self.create_test_dialog = QtWidgets.QDialog(self)
        self.create_test_dialog.setFont(QtGui.QFont('Times New Roman', 13))
        self.create_test_dialog.resize(400, 200)
        self.create_test_dialog.setWindowTitle('Создание названия теста')
        self.create_test_dialog.label = QtWidgets.QLabel('Введите название предмета')
        self.create_test_dialog.edit_text_name_bd = QtWidgets.QLineEdit()
        self.create_test_dialog.edit_text_name_bd.setPlaceholderText('Например Web-про граммирование')
        self.create_test_dialog.button_save = QtWidgets.QPushButton('Создать тест')
        self.create_test_dialog.button_save.clicked.connect(self.create_data_base)
        self.combo_groups = QtWidgets.QComboBox()
        self.combo_groups.addItems(["Не выбрано", "9-ПКС", '9-КСК', "9-ПБ", "9-ИБ", "9-C"])
        self.create_test_dialog.layout_db = QtWidgets.QVBoxLayout()
        self.create_test_dialog.layout_db.addWidget(self.create_test_dialog.label, 0, QtCore.Qt.AlignCenter)
        self.create_test_dialog.layout_db.addWidget(self.create_test_dialog.edit_text_name_bd)
        self.create_test_dialog.layout_db.addWidget(self.combo_groups)
        self.create_test_dialog.layout_db.addWidget(self.create_test_dialog.button_save)
        self.create_test_dialog.setLayout(self.create_test_dialog.layout_db)
        self.create_test_dialog.exec()

    def create_data_base(self):
        try:
            if self.combo_groups.currentText() == "Не выбрано":
                reply = QtWidgets.QMessageBox(self)
                reply.setFont(QtGui.QFont('Times New Roman', 13))
                reply.setIcon(QtWidgets.QMessageBox.Critical)
                reply.setWindowTitle("Выбирете группу")
                reply.setText('Выбирете которая будет выполнять тест')
                return reply.exec()

            DataBase.create_test(self.create_test_dialog.edit_text_name_bd.text(), self.combo_groups.currentText())
            self.choice_tests.addItems([self.create_test_dialog.edit_text_name_bd.text()])
            self.create_test_dialog.close()
        except pymysql.err.InternalError:
            reply = QtWidgets.QMessageBox(self)
            reply.setFont(QtGui.QFont('Times New Roman', 13))
            reply.setIcon(QtWidgets.QMessageBox.Critical)
            reply.setWindowTitle("Критическая ошибка названия теста")
            reply.setText("Данной название теста уже существует \nлибо переименуйте название либо обратитесь "
                          "к администратору")
            reply.show()
        except pymysql.err.ProgrammingError:
            return self.create_test_dialog.close()

    def edit_test_profile(self, points):
        def edit():
            # Изменение названия в базе данных и в конструкторе P.S. Добавить само изменение в базу данных
            DataBase.rename_test(self.choice_tests.itemAt(points).text(), self.rename_dialog.edit_caption.text())
            self.choice_tests.itemAt(points).setText(self.rename_dialog.edit_caption.text())
            self.rename_dialog.close()
            self.mains.right.choice_questions.setVisible(False)
        self.rename_dialog = QtWidgets.QDialog(self)
        self.rename_dialog.setFont(QtGui.QFont('Times New Roman', 13))
        self.rename_dialog.setWindowTitle('Окно редактирования')
        self.rename_dialog.resize(400, 100)
        self.rename_dialog.label_edit = QtWidgets.QLabel('Введите новое название теста', self)
        self.rename_dialog.edit_caption = QtWidgets.QLineEdit(self)
        self.rename_dialog.edit_caption.setPlaceholderText(self.choice_tests.itemAt(points).text())
        self.rename_dialog.edit_caption.setMaxLength(60)
        self.rename_dialog.accept_button = QtWidgets.QPushButton('Сохранить', self)
        self.rename_dialog.accept_button.clicked.connect(edit)
        self.rename_dialog.layout = QtWidgets.QVBoxLayout()
        self.rename_dialog.layout.addWidget(self.rename_dialog.label_edit)
        self.rename_dialog.layout.addWidget(self.rename_dialog.edit_caption)
        self.rename_dialog.layout.addWidget(self.rename_dialog.accept_button)
        self.rename_dialog.setLayout(self.rename_dialog.layout)
        self.rename_dialog.exec()


class MainWindows(QtWidgets.QMainWindow):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.setFixedSize(x_range_windows, y_range_windows)
        self.setWindowTitle('Test Create 3.0')
        self.setFont(QtGui.QFont('Times New Roman', 13))

        # В self.choice_tests будут дабавляться тесты по дисциплинам преподавателя
        self.left = LeftFrame(self)
        self.right = RightFrame(self)
        self.radio_box_create = CreateTest(self)
        splitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal)
        splitter.addWidget(self.left)
        splitter.addWidget(self.right)
        self.setCentralWidget(splitter)

        self.setMenuBar(Menu(self))

    def open_about(self, items):
        self.right.label_choice.setVisible(False)
        self.right.button_start.setVisible(True)
        # вывод данных из выбраной пользователем базы данных
        try:
            text = items.text()
        except AttributeError:
            text = items
        try:
            data_base_name = transliterate.translit(text, reversed=True)
            data_base_name = blank_name.sub('', data_base_name)
        except transliterate.exceptions.LanguageDetectionError:
            data_base_name = blank_name.sub('', text)
        profile_name.pop(4)
        profile_name.insert(4, data_base_name)

    def test_list_widget(self, items):
        try:
            text = items.text()
        except AttributeError:
            text = items
        try:
            data_base_name = transliterate.translit(text, reversed=True)
            data_base_name = blank_name.sub('', data_base_name)
        except transliterate.exceptions.LanguageDetectionError:
            data_base_name = blank_name.sub('', text)

        self.right.add_question_list_widget(DataBase.insert_question_to_app(data_base_name))


class Menu(QtWidgets.QMenuBar):
    def __init__(self, main, **kwargs):
        super().__init__(**kwargs)
        self.mains = main
        file_menu = self.addMenu('File')
        self.a = AuthenticationProfile()
        if profile_name[1] == 'Преподаватель':
            open_create_test = QtWidgets.QAction('Создать новый тест', self)
            open_create_test.setStatusTip('Create new test')
            open_create_test.triggered.connect(self.mains.left.table_add_to_database)
            file_menu.addAction(open_create_test)
            file_menu.addSeparator()

            test_select = QtWidgets.QAction('Создать тест с одним вариантом ответа', self)
            test_select.triggered.connect(lambda: self.mains.radio_box_create.value_checked(1))

            test_select_check = QtWidgets.QAction('Создать тест с несколькими вариантами ответа', self)
            test_select_check.triggered.connect(lambda: self.mains.radio_box_create.value_checked(2))

            file_menu_edit = self.addMenu('Тесты')
            file_menu_edit.addAction(test_select)
            file_menu_edit.addAction(test_select_check)

        close_file = QtWidgets.QAction('Закрыть программу', self)
        close_file.setStatusTip('Close test file')
        close_file.triggered.connect(lambda: sys.exit())
        file_menu.addAction(close_file)

        refresh_database = QtWidgets.QAction(QtGui.QIcon('1.jpg'), 'about', self)
        refresh_database.setStatusTip('about test create')

        refresh_attachment = QtWidgets.QAction('Обновление приложение', self)
        refresh_attachment.setStatusTip('Check for update')

        menu_about = self.addMenu('Help')
        menu_about.addAction(refresh_database)
        menu_about.addSeparator()
        menu_about.addAction(refresh_attachment)


class CreateTest:

    def __init__(self, main):
        self.main = main
        self.mains = main
        self.value_image = 0

    def value_checked(self, value_id):
        if self.main.right.choice_questions.isVisible():
            pass
        else:
            reply = QtWidgets.QMessageBox(self.main)
            reply.setFont(QtGui.QFont('Times New Roman', 13))
            reply.setIcon(QtWidgets.QMessageBox.Critical)
            reply.setWindowTitle("Ошибка")
            reply.setText('Выберете Тест для создания вопроса')
            return reply.exec()
        self.value_id = value_id
        if value_id == 1:
            self.radio_button_create()
            self.body_radio_box_create()
            self.layout_body_radio_box_create()
            self.map = self.radio_dialog
            self.radio_dialog.exec()

        elif value_id == 2:
            self.check_button_create()
            self.body_check_box_create()
            self.layout_body_check_box_create()
            self.map = self.check_dialog
            self.check_dialog.exec()

    def radio_button_create(self):
        self.edit_1 = QtWidgets.QTextEdit()
        self.radio_box_1 = QtWidgets.QRadioButton()
        self.layout_radio_box_1 = QtWidgets.QHBoxLayout()

        self.edit_2 = QtWidgets.QTextEdit()
        self.radio_box_2 = QtWidgets.QRadioButton()
        self.layout_radio_box_2 = QtWidgets.QHBoxLayout()

        self.edit_3 = QtWidgets.QTextEdit()
        self.radio_box_3 = QtWidgets.QRadioButton()
        self.layout_radio_box_3 = QtWidgets.QHBoxLayout()

        self.layout_radio_box_4 = QtWidgets.QHBoxLayout()
        self.edit_4 = QtWidgets.QTextEdit()
        self.radio_box_4 = QtWidgets.QRadioButton()

        self.layout_radio_box_5 = QtWidgets.QHBoxLayout()
        self.edit_5 = QtWidgets.QTextEdit()
        self.radio_box_5 = QtWidgets.QRadioButton()

        layout_box = [
            {
                "layout_name": [self.layout_radio_box_1, self.layout_radio_box_2, self.layout_radio_box_3,
                                self.layout_radio_box_4, self.layout_radio_box_5],
                "edit_text": [self.edit_1, self.edit_2, self.edit_3, self.edit_4, self.edit_5],
                "radio_box": [self.radio_box_1, self.radio_box_2, self.radio_box_3, self.radio_box_4,
                              self.radio_box_5],
                "number_id": 0},
            {
                "edit_visible": [self.edit_3, self.edit_4, self.edit_5],
                "radio_visible": [self.radio_box_3, self.radio_box_4, self.radio_box_5]
            }
                      ]

        for edit in layout_box[0]["edit_text"]:
            edit.clear()

        for layout_add in layout_box[0]["layout_name"]:
            layout_add.addWidget(layout_box[0]["radio_box"][layout_box[0]["number_id"]])
            layout_add.addSpacing(10)
            layout_add.addWidget(layout_box[0]["edit_text"][layout_box[0]["number_id"]])
            layout_box[0]["number_id"] += 1

        for box in layout_box[1]:
            for visible_box in layout_box[1][box]:
                visible_box.setVisible(False)

        layout_box[0]["number_id"] = 0
        self.button_group = QtWidgets.QButtonGroup()
        for box_add in layout_box[0]['radio_box']:
            layout_box[0]["number_id"] += 1
            self.button_group.addButton(box_add, layout_box[0]["number_id"])

        layout_box[0]["number_id"] = 0
        for box_edit in layout_box[0]['edit_text']:
            layout_box[0]["number_id"] += 1
            box_edit.setPlaceholderText('Введите сюда ' + str(layout_box[0]["number_id"]) + ' ответ')

    def body_radio_box_create(self):
        self.edit_question = QtWidgets.QTextEdit()
        self.edit_question.setPlaceholderText('Введите ваш вопрос')
        self.button_save = QtWidgets.QPushButton()
        self.button_save.setText('сохранить')
        self.button_save.clicked.connect(self.add_data_base)
        label = QtWidgets.QLabel()
        label.setText('сколько ответов в данном вопросе')
        combo = QtWidgets.QComboBox()
        combo.addItems(["2", "3", "4", "5"])
        combo.activated[str].connect(self.radio_button_checked)
        self.v_box = QtWidgets.QHBoxLayout()
        self.v_box.addWidget(label)
        self.v_box.addWidget(combo)
        self.v_box.addStretch(1)
        self.layout_button_image = QtWidgets.QHBoxLayout()
        self.button_image = QtWidgets.QPushButton('Добавить изображение')
        self.button_image.clicked.connect(self.open_image)
        self.button_clear_image = QtWidgets.QPushButton('Удалить изображение')
        self.button_clear_image.setVisible(False)
        self.button_clear_image.clicked.connect(self.del_image)
        self.pix_map = QtGui.QPixmap()
        self.image_label = QtWidgets.QLabel()
        self.image_label.setScaledContents(True)
        self.layout_button_image.addStretch(1)
        self.layout_button_image.addWidget(self.image_label)
        self.layout_button_image.addWidget(self.button_image)
        self.layout_button_image.addWidget(self.button_clear_image)

    def layout_body_radio_box_create(self):
        self.radio_dialog = QtWidgets.QDialog()
        self.radio_dialog.setWindowTitle('Вопрос для теста')
        self.radio_dialog.resize(851, 740)
        self.radio_dialog.setFont(QtGui.QFont('Times New Roman', 13))
        layout = QtWidgets.QVBoxLayout()
        layout.addSpacing(20)
        layout.addWidget(self.edit_question)
        layout_box = [self.layout_radio_box_1, self.layout_radio_box_2, self.layout_radio_box_3,
                      self.layout_radio_box_4, self.layout_radio_box_5, self.v_box, self.layout_button_image]
        for box in layout_box:
            layout.addSpacing(10)
            layout.addLayout(box)
        layout.addWidget(self.button_save)
        self.radio_dialog.setLayout(layout)

    def radio_button_checked(self, id_text):
        if id_text == '2':
            box_id_text = {'edit': [self.edit_3, self.edit_4, self.edit_5],
                           'radio': [self.radio_box_3, self.radio_box_4, self.radio_box_5]}
            for box_false in box_id_text:
                for i in box_id_text[box_false]:
                    i.setVisible(False)
                    i.setText('')
            for box_add in box_id_text['radio']:
                self.button_group.setId(box_add, 0)

        elif id_text == '3':
            box_id_text_true = [self.radio_box_3, self.edit_3]
            for box_true in box_id_text_true:
                box_true.setVisible(True)
            box_id_text_false = [self.radio_box_4, self.radio_box_5, self.edit_4, self.edit_5]
            for box_false in box_id_text_false:
                box_false.setVisible(False)
                box_false.setText('')
            box_add_radiobutton = {'radiobutton': [self.radio_box_4,
                                                   self.radio_box_5], 'id_radiobutton': 0}
            for box_add in box_add_radiobutton['radiobutton']:
                self.button_group.setId(box_add, box_add_radiobutton['id_radiobutton'])
                self.button_group.setId(self.radio_box_3, 3)

        elif id_text == '4':
            box_id_text_true = [self.radio_box_3, self.edit_3, self.radio_box_4, self.edit_4]
            for box_true in box_id_text_true:
                box_true.setVisible(True)

            box_id_text_false = [self.radio_box_5, self.edit_5]
            for box_false in box_id_text_false:
                box_false.setVisible(False)
                box_false.setText('')

            box_add_radiobutton = {'radiobutton': [self.radio_box_3, self.radio_box_4], 'id_radiobutton': 2}
            for box_add in box_add_radiobutton['radiobutton']:
                box_add_radiobutton['id_radiobutton'] += 1
                self.button_group.setId(box_add, box_add_radiobutton['id_radiobutton'])
                self.button_group.setId(self.radio_box_5, 0)

        elif id_text == '5':
            box_id_text_true = [self.radio_box_3, self.edit_3, self.radio_box_4, self.edit_4,
                                self.radio_box_5, self.edit_5]
            for box_true in box_id_text_true:
                box_true.setVisible(True)

            box_add_radiobutton = {'radiobutton': [self.radio_box_3, self.radio_box_4, self.radio_box_5],
                                   'id_radiobutton': 2}
            for box_add in box_add_radiobutton['radiobutton']:
                box_add_radiobutton['id_radiobutton'] += 1
                self.button_group.setId(box_add, box_add_radiobutton['id_radiobutton'])

    def check_button_create(self):
        self.edit_1 = QtWidgets.QTextEdit()
        self.radio_box_1 = QtWidgets.QCheckBox()
        self.layout_radio_box_1 = QtWidgets.QHBoxLayout()

        self.edit_2 = QtWidgets.QTextEdit()
        self.radio_box_2 = QtWidgets.QCheckBox()
        self.layout_radio_box_2 = QtWidgets.QHBoxLayout()

        self.edit_3 = QtWidgets.QTextEdit()
        self.radio_box_3 = QtWidgets.QCheckBox()
        self.layout_radio_box_3 = QtWidgets.QHBoxLayout()

        self.layout_radio_box_4 = QtWidgets.QHBoxLayout()
        self.edit_4 = QtWidgets.QTextEdit()
        self.radio_box_4 = QtWidgets.QCheckBox()

        self.layout_radio_box_5 = QtWidgets.QHBoxLayout()
        self.edit_5 = QtWidgets.QTextEdit()
        self.radio_box_5 = QtWidgets.QCheckBox()

        layout_box = [
            {
                "layout_name": [self.layout_radio_box_1, self.layout_radio_box_2, self.layout_radio_box_3,
                                self.layout_radio_box_4, self.layout_radio_box_5],
                "edit_text": [self.edit_1, self.edit_2, self.edit_3, self.edit_4, self.edit_5],
                "radio_box": [self.radio_box_1, self.radio_box_2, self.radio_box_3, self.radio_box_4,
                              self.radio_box_5],
                "number_id": 0},
            {
                "edit_visible": [self.edit_4, self.edit_5],
                "radio_visible": [self.radio_box_4, self.radio_box_5]
            }
                      ]

        for layout_add in layout_box[0]["layout_name"]:
            layout_add.addWidget(layout_box[0]["radio_box"][layout_box[0]["number_id"]])
            layout_add.addSpacing(10)
            layout_add.addWidget(layout_box[0]["edit_text"][layout_box[0]["number_id"]])
            layout_box[0]["number_id"] += 1

        for box in layout_box[1]:
            for visible_box in layout_box[1][box]:
                visible_box.setVisible(False)

        layout_box[0]["number_id"] = 0
        for box_edit in layout_box[0]['edit_text']:
            layout_box[0]["number_id"] += 1
            box_edit.setPlaceholderText('Введите сюда ' + str(layout_box[0]["number_id"]) + ' ответ')

    def body_check_box_create(self):
        self.edit_question = QtWidgets.QTextEdit()
        self.edit_question.setPlaceholderText('Введите ваш вопрос')
        self.button_save = QtWidgets.QPushButton()
        self.button_save.setText('сохранить')
        self.button_save.clicked.connect(self.add_data_base)
        label = QtWidgets.QLabel()
        label.setText('сколько ответов в данном вопросе')
        combo = QtWidgets.QComboBox()
        combo.addItems(["3", "4", "5"])
        combo.activated[str].connect(self.checkbox_button_checked)
        self.v_box = QtWidgets.QHBoxLayout()
        self.v_box.addWidget(label)
        self.v_box.addWidget(combo)
        self.v_box.addStretch(1)
        self.layout_button_image = QtWidgets.QHBoxLayout()
        self.button_image = QtWidgets.QPushButton('Добавить изображение')
        self.button_image.clicked.connect(self.open_image)
        self.button_clear_image = QtWidgets.QPushButton('Удалить изображение')
        self.button_clear_image.setVisible(False)
        self.button_clear_image.clicked.connect(self.del_image)
        self.pix_map = QtGui.QPixmap()
        self.image_label = QtWidgets.QLabel()
        self.image_label.setScaledContents(True)
        self.layout_button_image.addStretch(1)
        self.layout_button_image.addWidget(self.image_label)
        self.layout_button_image.addWidget(self.button_image)
        self.layout_button_image.addWidget(self.button_clear_image)

    def layout_body_check_box_create(self):
        self.check_dialog = QtWidgets.QDialog()
        self.check_dialog.setWindowTitle('Вопрос для теста')
        self.check_dialog.resize(851, 740)
        self.check_dialog.setFont(QtGui.QFont('Times New Roman', 13))
        layout = QtWidgets.QVBoxLayout()
        layout.addSpacing(20)
        layout.addWidget(self.edit_question)
        layout_box = [self.layout_radio_box_1, self.layout_radio_box_2, self.layout_radio_box_3,
                      self.layout_radio_box_4, self.layout_radio_box_5, self.v_box, self.layout_button_image]
        for box in layout_box:
            layout.addSpacing(10)
            layout.addLayout(box)
        layout.addWidget(self.button_save)
        self.check_dialog.setLayout(layout)

    def checkbox_button_checked(self, id_text):
        if id_text == '3':
            box_id = {"radio_box": [self.radio_box_4, self.radio_box_5], "edit_text": [self.edit_4, self.edit_5]}
            for box_false in box_id:
                for visible in box_id[box_false]:
                    visible.setVisible(False)
                    visible.setText('')
            for box_add in box_id["radio_box"]:
                box_add.setChecked(False)

        elif id_text == '4':
            box_id = [{"radio_box": [self.radio_box_4], "edit_text": [self.edit_4]},
                      {"visible_false": [self.radio_box_5, self.edit_5]}]
            for box_true in box_id[0]:
                for visible in box_id[0][box_true]:
                    visible.setVisible(True)

            for box_false in box_id[1]["visible_false"]:
                box_false.setVisible(False)
                box_false.setText('')
                self.radio_box_5.setChecked(False)

        elif id_text == '5':
            box_id_text_true = [self.radio_box_4, self.edit_4,
                                self.radio_box_5, self.edit_5]
            for box_true in box_id_text_true:
                box_true.setVisible(True)

    def open_image(self):
        file_name = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', '', "Images (*.xpm *.jpg *.gif)")[0]
        if file_name:
            self.value_image = 1
            self.button_image.setText('Изменить изображение')
            self.button_clear_image.setVisible(True)
            file = open(file_name, "rb")
            with file:
                self.img_data = file.read()
                self.pix_map.loadFromData(self.img_data)
                self.image_label.setPixmap(self.pix_map)
                self.image_label.setFixedSize(80, 40)
                self.image_label.setToolTip('<img src=' + file_name + '></img>')

    def del_image(self):
        self.value_image = 0
        self.button_clear_image.setVisible(False)
        self.image_label.clear()
        self.button_image.setText('Добавить изображение')

    def add_data_base(self):
        if not (self.edit_question.toPlainText() and self.edit_question.toPlainText().strip()):
            self.edit_question.setToolTip('<h2>Заполните вопрос</h2>')
            return QtCore.QTimer.singleShot(1, lambda: QtWidgets.QToolTip.showText(
                self.map.mapToGlobal(self.edit_question.pos()), self.edit_question.toolTip(),
                self.edit_question, QtCore.QRect()))

        if not (self.edit_1.toPlainText() and self.edit_1.toPlainText().strip()):
            self.edit_1.setToolTip('<h2>Заполните 1й ответ</h2>')
            return QtCore.QTimer.singleShot(1, lambda: QtWidgets.QToolTip.showText(
                self.map.mapToGlobal(self.edit_1.pos()), self.edit_1.toolTip(), self.edit_1, QtCore.QRect()))

        if not (self.edit_2.toPlainText() and self.edit_1.toPlainText().strip()):
            self.edit_2.setToolTip('<h2>Заполните 2й ответ</h2>')
            return QtCore.QTimer.singleShot(1, lambda: QtWidgets.QToolTip.showText(
                self.map.mapToGlobal(self.edit_2.pos()), self.edit_2.toolTip(), self.edit_2, QtCore.QRect()))

        if self.value_id == 1:
            if self.button_group.checkedId() == 0 or self.button_group.checkedId() == -1:
                self.radio_box_1.setToolTip('<h2>Заполните правильный ответ</h2>')
                return QtCore.QTimer.singleShot(1, lambda: QtWidgets.QToolTip.showText(
                    self.map.mapToGlobal(self.radio_box_1.pos()), self.radio_box_1.toolTip(),
                    self.radio_box_1, QtCore.QRect()))
            self.db_radio_text = self.button_group.checkedId()
        else:
            if not (self.edit_3.toPlainText() and self.edit_1.toPlainText().strip()):
                self.edit_3.setToolTip('<h2>Заполните 3й ответ</h2>')
                return QtCore.QTimer.singleShot(1, lambda: QtWidgets.QToolTip.showText(
                    self.map.mapToGlobal(self.edit_3.pos()), self.edit_3.toolTip(), self.edit_3, QtCore.QRect()))

            self.db_radio_text = []
            if self.radio_box_1.isChecked():
                self.db_radio_text.append('1')
            if self.radio_box_2.isChecked():
                self.db_radio_text.append('2')
            if self.radio_box_3.isChecked():
                self.db_radio_text.append('3')
            if self.radio_box_4.isChecked():
                self.db_radio_text.append('4')
            if self.radio_box_5.isChecked():
                self.db_radio_text.append('5')

            if not self.db_radio_text:
                self.radio_box_1.setToolTip('<h2>Заполните правильный вариант ответа</h2>')
                return QtCore.QTimer.singleShot(1, lambda: QtWidgets.QToolTip.showText(
                    self.map.mapToGlobal(self.radio_box_1.pos()), self.radio_box_1.toolTip(), self.radio_box_1,
                    QtCore.QRect()))
            self.db_radio_text = str(self.db_radio_text)

        try:
            if self.value_image:
                DataBase.create_question_test(self.edit_question.toPlainText(), self.edit_1.toPlainText(),
                                              self.edit_2.toPlainText(), self.edit_3.toPlainText(),
                                              self.edit_4.toPlainText(), self.edit_5.toPlainText(),
                                              self.db_radio_text, self.img_data, self.value_id)
            else:
                DataBase.create_question_test(self.edit_question.toPlainText(), self.edit_1.toPlainText(),
                                              self.edit_2.toPlainText(), self.edit_3.toPlainText(),
                                              self.edit_4.toPlainText(), self.edit_5.toPlainText(),
                                              self.db_radio_text, None, self.value_id)

            self.mains.test_list_widget(profile_name[4])
            if self.value_id == 1:
                self.radio_dialog.close()
            elif self.value_id == 2:
                self.check_dialog.close()
        except pymysql.err.ProgrammingError:
            reply = QtWidgets.QMessageBox(self)
            reply.setFont(QtGui.QFont('Times New Roman', 13))
            reply.setIcon(QtWidgets.QMessageBox.Critical)
            reply.setWindowTitle("Ошибка")
            reply.setText('Для записи данных выберите базу для сохранения')
            reply.show()
            self.close()


class StudentTest(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.hours, self.minutes, self.seconds, self.answer = 0, 0, 5, []
        self.setFixedSize(800, 800)

        self.text_question = QtWidgets.QLabel('<h1>Вопрос к тесту</h1>')

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.start_time)

        self.pix_map = QtGui.QPixmap()
        self.text_image = QtWidgets.QLabel()

        self.label_time = QtWidgets.QLabel()
        self.label_time.setText('%02d : %02d : %02d' % (self.hours, self.minutes, self.seconds))
        self.label_time.setFont(QtGui.QFont("Times New Roman", 24))

        self.radio_box_number_1 = QtWidgets.QRadioButton('1')
        self.radio_box_number_2 = QtWidgets.QRadioButton('2')
        self.radio_box_number_3 = QtWidgets.QRadioButton('3')
        self.radio_box_number_4 = QtWidgets.QRadioButton('4')
        self.radio_box_number_5 = QtWidgets.QRadioButton('5')

        self.check_box_1 = QtWidgets.QCheckBox('1')
        self.check_box_2 = QtWidgets.QCheckBox('2')
        self.check_box_3 = QtWidgets.QCheckBox('3')
        self.check_box_4 = QtWidgets.QCheckBox('4')
        self.check_box_5 = QtWidgets.QCheckBox('5')

        self.entry_number_1 = QtWidgets.QLineEdit()
        self.entry_number_2 = QtWidgets.QLineEdit()
        self.entry_number_3 = QtWidgets.QLineEdit()
        self.entry_number_4 = QtWidgets.QLineEdit()
        self.entry_number_5 = QtWidgets.QLineEdit()

        self.push_start = QtWidgets.QPushButton('Начать тестирование')
        self.push_start.clicked.connect(self.start_question)

        self.push_next = QtWidgets.QCommandLinkButton('Следующий вопрос')
        self.push_next.clicked.connect(self.profile_answer)
        self.push_next.setVisible(False)

        self.push_stop = QtWidgets.QPushButton('Окончить тест')
        self.push_stop.clicked.connect(self.answer_print)
        self.push_stop.setVisible(False)

        self.test = [i for i in DataBase.connect_client_question(profile_name[4])]

        self.setLayout(self.layout_widget())

    def layout_widget(self):
        self.all_widget_layout = {"radio_box": [self.radio_box_number_1, self.radio_box_number_2,
                                                self.radio_box_number_3, self.radio_box_number_4,
                                                self.radio_box_number_5],
                                  "check_box": [self.check_box_1, self.check_box_2, self.check_box_3,
                                                self.check_box_4, self.check_box_5],
                                  "entry_box": [self.entry_number_1, self.entry_number_2, self.entry_number_3,
                                                self.entry_number_4, self.entry_number_5]}

        all_layout = QtWidgets.QVBoxLayout()

        self.button_group = QtWidgets.QButtonGroup()
        [self.button_group.addButton(box_add, number + 1) for number, box_add in
         enumerate(self.all_widget_layout["radio_box"])]

        all_layout.addWidget(self.label_time, 0, QtCore.Qt.AlignCenter | QtCore.Qt.AlignTop)
        all_layout.addWidget(self.text_question, 0, QtCore.Qt.AlignTop)
        all_layout.addWidget(self.text_image)

        random_widget = self.all_widget_layout["radio_box"] + self.all_widget_layout["check_box"]

        items = [i for i in range(len(random_widget))]
        random.SystemRandom().shuffle(items)

        [all_layout.addWidget(random_widget[add_widget]) for add_widget in items]

        [all_layout.addWidget(i) for i in self.all_widget_layout["entry_box"]]

        [widget_visible_false.setVisible(False) for widget_visible_false in
         self.all_widget_layout["entry_box"] + random_widget]

        all_layout.addWidget(self.push_start, 0, QtCore.Qt.AlignRight | QtCore.Qt.AlignBottom)
        all_layout.addWidget(self.push_next, 0, QtCore.Qt.AlignRight | QtCore.Qt.AlignBottom)
        all_layout.addWidget(self.push_stop, 0, QtCore.Qt.AlignRight | QtCore.Qt.AlignBottom)

        return all_layout

    def start_time(self):
        if self.seconds == 0:
            if self.minutes == 0:
                if self.hours == 0:
                    self.label_time.setText('СТОП!')
                    self.timer.stop()

                    [check_box.setEnabled(False) for check_box in self.all_widget_layout["check_box"]]
                    [radio_box.setEnabled(False) for radio_box in self.all_widget_layout["radio_box"]]

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

    def start_question(self):
        self.timer.start(1000)
        self.push_start.setVisible(False)
        self.push_next.setVisible(True)
        self.next_question()

    def answer_print(self):
        QtWidgets.QMessageBox.information(self, 'Вывод', str(self.answer.count("+")) + ' правильных ответов.'
                                                                                       '\nТест окончен')
        self.close()

    def next_question(self):
        # Формирование теста 1 с одни ответом 2 с несколькими
        try:
            self.question = self.test[0]
            if self.question[7] == 1:
                [check_box.setVisible(False) for check_box in self.all_widget_layout["check_box"]]
                [radio_box.setVisible(True) for radio_box in self.all_widget_layout["radio_box"]]

                if self.question[3] == "":
                    [radio_box.setVisible(False) for radio_box in self.all_widget_layout["radio_box"][2:]]
                elif self.question[4] == "":
                    [radio_box.setVisible(False) for radio_box in self.all_widget_layout["radio_box"][3:]]
                elif self.question[5] == "":
                    [radio_box.setVisible(False) for radio_box in self.all_widget_layout["radio_box"][4:]]

                [widget.setText(self.question[j+1]) for j, widget in enumerate(self.all_widget_layout["radio_box"])]

            elif self.question[7] == 2:
                [check_box.setVisible(True) for check_box in self.all_widget_layout["check_box"]]
                [radio_box.setVisible(False) for radio_box in self.all_widget_layout["radio_box"]]

                if self.question[4] == "":
                    [check_box.setVisible(False) for check_box in self.all_widget_layout["check_box"][3:]]
                elif self.question[5] == "":
                    [check_box.setVisible(False) for check_box in self.all_widget_layout["check_box"][4:]]

                [widget.setText(self.question[j + 1]) for j, widget in enumerate(self.all_widget_layout["check_box"])]

            self.text_question.setText("<h1>{}</h1>".format(self.question[0]))
            self.pix_map.loadFromData(self.question[8])
            self.text_image.setPixmap(self.pix_map)
            self.test.remove(self.question)

        except IndexError:
            self.timer.stop()
            [check_box.setEnabled(False) for check_box in self.box_selected["check_box"]]

            [radio_box.setVisible(False) for radio_box in self.all_widget_layout["radio_box"]]

    def profile_answer(self):
        if self.question[7] == 1:
            if self.button_group.checkedId() == int(self.question[6]):
                self.answer.append("+")
            else:
                self.answer.append('-')
        elif self.question[7] == 2:
            self.db_radio_text = []
            if self.check_box_1.isChecked():
                self.db_radio_text.append('1')
                self.check_box_1.setChecked(False)
            if self.check_box_2.isChecked():
                self.db_radio_text.append('2')
                self.check_box_2.setChecked(False)
            if self.check_box_3.isChecked():
                self.db_radio_text.append('3')
                self.check_box_3.setChecked(False)
            if self.check_box_4.isChecked():
                self.db_radio_text.append('4')
                self.check_box_4.setChecked(False)
            if self.check_box_5.isChecked():
                self.db_radio_text.append('5')
                self.check_box_5.setChecked(False)
            if str(self.db_radio_text) == self.question[6]:
                self.answer.append('+')
            else:
                self.answer.append('-')
        if len(self.test) == 0:
            self.timer.stop()
            self.push_stop.setVisible(True)
            self.push_next.setVisible(False)
        else:
            self.next_question()
        print(self.answer)


class DataBase:
    @staticmethod
    def insert_question_to_app(name_base):
        # Добавление в вопросов в choice_question
        try:
            data_base_name = transliterate.translit(name_base, reversed=True)
            data_base_name = blank_name.sub('', data_base_name)
        except transliterate.exceptions.LanguageDetectionError:
            data_base_name = blank_name.sub('', name_base)
        with pymysql.connect(host=host,
                             port=3306,
                             user=user,
                             password=password,
                             db="test",
                             charset='utf8') as cur:
            cur.execute("SELECT question, answer_1, answer_2, answer_3, answer_4, answer_5, number_answer "
                        "FROM %s" % data_base_name)
            profile_name.pop(4)
            profile_name.insert(4, data_base_name)
        return cur.fetchall()

    @staticmethod
    def delete_question(name_question):
        # удаляет вопрос
        with pymysql.connect(
                host=host,
                port=3306,
                user=user,
                password=password,
                db="test",
                charset='utf8') as con:
            con.execute("DELETE FROM %s WHERE question = '%s'"
                        % (profile_name[4], name_question))
        return True

    @staticmethod
    def add_to_list_question():
        # добавляет в choice_test Базы данны
        with pymysql.connect(
                host=host,
                port=3306,
                user=user,
                password=password,
                db="test_create",
                charset='utf8') as con:
            if profile_name[1] == "Преподаватель":
                con.execute("SELECT real_name_test FROM %s" % profile_name[3])
            else:
                con.execute("SELECT Name_test FROM All_base "
                            "WHERE Group_name REGEXP %s AND Ready LIKE 1", (profile_name[2]))
            return con.fetchall()

    @staticmethod
    def connect_to_data_base(login_name, password_name):
        with pymysql.connect(
             host=host,
             port=3306,
             user=user,
             password=password,
             db="test_create",
             charset='utf8') as cur:
            cur.execute("SELECT Surname, Position, Groups, name_table FROM authentication "
                        "WHERE Login LIKE %s AND Password LIKE %s", (login_name, password_name))
            return cur.fetchall()

    @staticmethod
    def delete_test(test_name):
        try:
            data_base_name = transliterate.translit(test_name, reversed=True)
            data_base_name = blank_name.sub('', data_base_name)
        except transliterate.exceptions.LanguageDetectionError:
            data_base_name = blank_name.sub('', test_name)
        with pymysql.connect(
                host=host,
                port=3306,
                user=user,
                password=password,
                db="test",
                charset='utf8') as conn, pymysql.connect(
                                                         host=host,
                                                         port=3306,
                                                         user=user,
                                                         password=password,
                                                         db="test_create",
                                                         charset='utf8') as con:
            conn.execute("DROP TABLE %s" % data_base_name)
            con.execute("DELETE FROM %s WHERE real_name_test = '%s'" % (profile_name[3], test_name))
            con.execute("DELETE FROM All_base WHERE Name_test = '%s'" % test_name)
        return

    @staticmethod
    def create_test(name_test, groups_name):
        try:
            data_base_name = transliterate.translit(name_test, reversed=True)
            data_base_name = blank_name.sub('', data_base_name)
        except transliterate.exceptions.LanguageDetectionError:
            data_base_name = blank_name.sub('', name_test)
        with pymysql.connect(host=host,
                             port=3306,
                             user=user,
                             password=password,
                             db="test",
                             charset='utf8') as cur:

                cur.execute('CREATE TABLE  %s '
                            '(ID	INTEGER PRIMARY KEY NOT NULL AUTO_INCREMENT,'
                            'question	CHAR ( 50 ),'
                            'answer_1	CHAR ( 50 ),'
                            'answer_2	CHAR ( 50 ),'
                            'answer_3	CHAR ( 50 ),'
                            'answer_4	CHAR ( 50 ),'
                            'answer_5	CHAR ( 50 ),'
                            'number_answer	CHAR ( 50 ),'
                            'type_question	INTEGER,'
                            'image	BLOB'')' % data_base_name)
                cur.close()
                with pymysql.connect(host=host,
                                     port=3306,
                                     user=user,
                                     password=password,
                                     db="test_create",
                                     charset='utf8') as create:
                    create.execute("INSERT INTO " + profile_name[3] + " (ID, real_name_test) VALUE(NULL, %s)",
                                   name_test)
                    create.execute("INSERT INTO All_base (Name_test, Group_name, Ready) VALUE(%s, %s, %s)",
                                   (name_test, groups_name, '1'))
                    create.close()

    @staticmethod
    def rename_test(name_test, rename_test):
        try:
            data_base_name = blank_name.sub('', transliterate.translit(name_test, reversed=True))
        except transliterate.exceptions.LanguageDetectionError:
            data_base_name = blank_name.sub('', name_test)
        try:
            data_base_name_rename = blank_name.sub('', transliterate.translit(rename_test, reversed=True))
        except transliterate.exceptions.LanguageDetectionError:
            data_base_name_rename = blank_name.sub('', rename_test)

        with pymysql.connect(host=host,
                             port=3306,
                             user=user,
                             password=password,
                             db="test_create",
                             charset='utf8',
                             autocommit=True) as cur, pymysql.connect(host=host,
                                                                      port=3306,
                                                                      user=user,
                                                                      password=password,
                                                                      db="test",
                                                                      charset='utf8') as conn:
            cur.execute("UPDATE %s SET real_name_test = '%s' WHERE real_name_test = '%s'"
                        % (profile_name[3], rename_test, name_test))
            cur.execute("UPDATE All_base SET Name_test = '%s' WHERE Name_test = '%s'"
                        % (rename_test, name_test))
            conn.execute("RENAME TABLE %s TO %s" % (data_base_name, data_base_name_rename))
        return

    @staticmethod
    def create_question_test(question, answer_1, answer_2, answer_3, answer_4, answer_5, number_answer, image, set_box):
        with pymysql.connect(
                             host=host,
                             port=3306,
                             user=user,
                             password=password,
                             db="test",
                             charset='utf8') as cur:
            # data_base = название базы данных которая сейчас используется
            cur.execute(
                'INSERT INTO ' + profile_name[4] + ' (ID,  question, answer_1, answer_2, answer_3, answer_4,'
                                                   'answer_5, number_answer, type_question, image) '
                                                   'VALUES (NULL,  %s, %s, %s, %s, %s,  %s, %s, %s, %s)',
                (question, answer_1, answer_2, answer_3, answer_4, answer_5, number_answer, set_box, image))
            return

    @staticmethod
    def connect_client_question(items):
        try:
            text = items.text()
        except AttributeError:
            text = items
        try:
            data_base_name = transliterate.translit(text, reversed=True)
            data_base_name = blank_name.sub('', data_base_name)
        except transliterate.exceptions.LanguageDetectionError:
            data_base_name = blank_name.sub('', text)

        with pymysql.connect(host=host,
                             port=3306,
                             user=user,
                             password=password,
                             db="test",
                             charset='utf8') as cur:
            cur.execute("SELECT question, answer_1, answer_2, answer_3, answer_4, answer_5, number_answer,"
                        " type_question, image FROM %s " % data_base_name)

            test_question = cur.fetchall()

            test_random = list(set(test_question))
            random.shuffle(test_random)
            random.SystemRandom().shuffle(test_random)

            return test_random[0:20]


def update_configuration_text_text():
    configuration_text.clear()
    configuration_text.append(config.get('font', 'font_family'))
    configuration_text.append(int(config.get('font', 'font_size')))


if __name__ == "__main__":
    configuration_text, blank_name, profile_name = [], re.compile("[^a-zA-Z,\d]"), \
                                                   ['Admin Panel', 'Преподаватель', 'None', 'AdminTest', 'adminbase']
    config = configparser.ConfigParser()
    config.read('cfg.ini', encoding='utf-8-sig')
    host = config.get('mysql', 'email')
    user = config.get('mysql', 'user')
    password = config.get('mysql', 'password')
    update_configuration_text_text()
    app = QtWidgets.QApplication(sys.argv)
    windows = QtWidgets.QDesktopWidget().availableGeometry()
    x_global_range = 0
    x_range_windows = windows.width() - 100
    y_range_windows = windows.height() - 100
    ma = AuthenticationProfile()
    ma.show()
    sys.exit(app.exec_())
