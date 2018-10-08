import sys
from PyQt5 import QtWidgets


class Main(QtWidgets.QListWidget):
    def __init__(self):
        super().__init__()
        self.resize(600, 450)
        self.addItems([str(i) for i in range(10)])
        self.setSpacing(4)
        self.setStyleSheet("""
            QListWidget{
                border: 0px;
                background: #F0F0F0;
                font-size: 20px;
                font-family: Times New Roman;
                padding: 5px;
            }
            QListWidget::item {
                background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                            stop: 0 #FAFBFE, stop: 1 #DCDEF1);
                border-style: outset;
                border-radius: 10px;
                border-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                            stop: 0 #FAFBFE, stop: 1 #DCDEF1);
                font: bold 14px;
                min-width: 10em;
                padding: 6px;
            }
            QListWidget::item:selected {
                 border: 1px solid #6a6ea9;
                 color: #000;
            }
        """)
        
        # sky color
        """
            QListWidget{
                border: 0px;
                background: #F0F0F0;
                font-size: 20px;
                font-family: Times New Roman;
                padding: 5px;
            }
            QListWidget::item {
                background-color: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                                            stop: 0 #5af, stop: 1 #fff);
                border-style: outset;
                border-radius: 10px;
                border-color: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                                            stop: 0 #5af, stop: 1 #fff);
                font: bold 14px;
                min-width: 10em;
                padding: 6px;
            }
            QListWidget::item:selected {
                 border: 1px solid #6a6ea9;
                 color: #000;
            }
        """


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main = Main()
    main.show()
    sys.exit(app.exec_())
