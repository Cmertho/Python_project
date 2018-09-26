import sys
from PyQt5 import QtWidgets


class Calculate(object):
    ENGLISH_CALCULATE = r"""qwertyuiop[]asdfghjkl;'zxcvbnm,./QWERTYUIOP[]ASDFGHJKL;'ZXCVBNM,./`
    1234567890-=\~!@#$%^&*()_+|"""
    RUSSIAN_CALCULATE = r"""йцукенгшщзхъфывапролджэячсмитьбю.ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ.ё
    1234567890-=\Ё!"№;%:?*()_+/"""

    def convert_russian_to_english(self, text):
        convert_english_text = ''
        for i in text:
            if i == " ":
                convert_english_text += " "
                continue
            elif i == "\n":
                convert_english_text += "\n"
                continue
            elif i == "\t":
                convert_english_text += '\t'
                continue
            convert_english_text += self.ENGLISH_CALCULATE[self.RUSSIAN_CALCULATE.index(i)]
        return convert_english_text

    def convert_english_to_russian(self, text):
        convert_russian_text = ""
        for i in text:
            if i == " ":
                convert_russian_text += " "
                continue
            elif i == "\n":
                convert_russian_text += "\n"
                continue
            elif i == "\t":
                convert_russian_text += '\t'
                continue
            convert_russian_text += self.RUSSIAN_CALCULATE[self.ENGLISH_CALCULATE.index(i)]
        return convert_russian_text


class Main(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.convert = Calculate()
        self.initUI()

    def initUI(self):
        self.setStyleSheet("font-size:20px;")
        label_rus = QtWidgets.QLabel("Вводимые русские символы")
        self.line_russian_text = QtWidgets.QPlainTextEdit()
        label_eng = QtWidgets.QLabel("Enter english characters")
        self.line_english_text = QtWidgets.QPlainTextEdit()
        button = QtWidgets.QPushButton("Конвертировать")
        button.clicked.connect(self.convert_text)
        button_clear = QtWidgets.QPushButton("Стереть")
        button_clear.clicked.connect(lambda: self.line_russian_text.clear())
        button_clear.clicked.connect(lambda: self.line_english_text.clear())
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(label_rus)
        layout.addWidget(self.line_russian_text)
        layout.addWidget(label_eng)
        layout.addWidget(self.line_english_text)
        layout.addWidget(button)
        layout.addWidget(button_clear)
        self.setLayout(layout)

    def convert_text(self):
        if not self.line_english_text.toPlainText():
            self.line_english_text.setPlainText(self.convert.convert_russian_to_english(
                self.line_russian_text.toPlainText()))
            return self.line_russian_text.clear()
        self.line_russian_text.setPlainText(self.convert.convert_english_to_russian(
            self.line_english_text.toPlainText()))
        return self.line_english_text.clear()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main = Main()
    main.show()
    sys.exit(app.exec_())
