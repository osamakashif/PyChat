__author__ = 'Osama Kashif'
__version__ = '1.0.0'

import sys
from PyQt5.QtWidgets import (QApplication, QWidget)
from connection import Connection


class Chat(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.window = Connection()
        self.window.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Chat()
    sys.exit(app.exec_())
