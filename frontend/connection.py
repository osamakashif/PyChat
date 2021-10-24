__author__ = 'Osama Kashif'
__version__ = '1.0.0'

from PyQt5.QtWidgets import (QWidget, QGridLayout, QLabel, QLineEdit, QPushButton, QMessageBox)
from PyQt5.QtCore import QCoreApplication, QThread
from backend.client import ChatClient
from frontend.connected import Connected

class Connection(QWidget):
    
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        grid = QGridLayout()
        self.setLayout(grid)

        self.ipAdd = QLineEdit()
        self.port = QLineEdit()
        self.nickname = QLineEdit()
        grid.addWidget(QLabel('IP Address'), 0, 0)
        grid.addWidget(QLabel('Port'), 1, 0)
        grid.addWidget(QLabel('Nickname'), 2, 0)

        grid.addWidget(self.ipAdd, 0, 1)
        grid.addWidget(self.port, 1, 1)
        grid.addWidget(self.nickname, 2, 1)

        connectBtn = QPushButton('Connect', self)
        connectBtn.resize(connectBtn.sizeHint())
        connectBtn.clicked.connect(self.toConnected)

        cancelBtn = QPushButton('Cancel', self)
        cancelBtn.resize(cancelBtn.sizeHint())
        cancelBtn.clicked.connect(self.close)

        grid.addWidget(connectBtn, 3, 2)
        grid.addWidget(cancelBtn, 3, 3)

        self.setWindowTitle('Chat')
        self.setGeometry(300, 300, 500, 250)
        self.show()
    
    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message', 'Are you sure to quit?',
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:        event.accept()
        else:                               event.ignore()

    def toConnected(self):                       # +++
        ipAddress = self.ipAdd.text()
        portNumber = int(self.port.text())
        nick = self.nickname.text()
        if (ipAddress == ""):
            client = ChatClient(nick, portNumber)
        else:
            client = ChatClient(nick, portNumber, ipAddress)
        self.connected = Connected(client, self)
        self.ipAdd.clear()
        self.port.clear()
        self.nickname.clear()
        self.connected.show()
        self.hide()