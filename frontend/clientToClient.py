__author__ = 'Osama Kashif'
__version__ = '1.0.0'

from PyQt5.QtWidgets import (QWidget, QLineEdit, QLabel, QPushButton, QHBoxLayout, QVBoxLayout, QTextEdit, QLabel)

class ClientToClient(QWidget):     
    
    def __init__(self, client, previousScreen):
        super().__init__()
        self.initUI(client, previousScreen)

    def initUI(self, client, previousScreen):
        self.connected = previousScreen
        self.client = client
        # print("Client:")
        # print(client)
        # chat1_1Btn = QPushButton('1:1 Chat', self)
        # chat1_1Btn.resize(chat1_1Btn.sizeHint())
        sendBtn = QPushButton('Send', self)
        sendBtn.resize(sendBtn.sizeHint())

        closeBtn = QPushButton('Close', self)
        closeBtn.resize(closeBtn.sizeHint())
        # closeBtn.clicked.connect()??????????????????????????????????????
        
        self.sendBox = QLineEdit()

        hbox = QHBoxLayout()
        hbox.addWidget(self.sendBox)
        hbox.addWidget(sendBtn)
        vbox = QVBoxLayout()
        chatHistory = QTextEdit()
        vbox.addWidget(QLabel("Chat with "+ str(client[0][2])))
        vbox.addWidget(chatHistory)
        vbox.addLayout(hbox)
        vbox.addWidget(closeBtn)

        self.setLayout(vbox)

    def close(self):
        self.hide()
        self.connected.show()