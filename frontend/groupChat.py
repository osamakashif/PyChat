__author__ = 'Osama Kashif'
__version__ = '1.0.0'

from PyQt5.QtWidgets import (QWidget, QLineEdit, QLabel, QPushButton, QHBoxLayout, QVBoxLayout, QTextEdit, QLabel)

class GroupChat(QWidget):     
    
    def __init__(self, group):
        super().__init__()
        self.initUI(group)

    def initUI(self, group):

        # chat1_1Btn = QPushButton('1:1 Chat', self)
        # chat1_1Btn.resize(chat1_1Btn.sizeHint())
        sendBtn = QPushButton('Send', self)
        sendBtn.resize(sendBtn.sizeHint())

        closeBtn = QPushButton('Close', self)
        closeBtn.resize(closeBtn.sizeHint())
        # closeBtn.clicked.connect()??????????????????????????????????????
        
        self.sendBox = QLineEdit()

        hbox1 = QHBoxLayout()
        hbox1.addWidget(self.sendBox)
        hbox1.addWidget(sendBtn)
        vbox1 = QVBoxLayout()
        chatHistory = QTextEdit()
        vbox1.addWidget(QLabel(group.getFullName()))
        vbox1.addWidget(chatHistory)
        vbox1.addLayout(hbox1)
        vbox1.addWidget(closeBtn)

        vbox2 = QVBoxLayout()
        inviteBtn = QPushButton('Invite', self)
        inviteBtn.resize(inviteBtn.sizeHint())
        # inviteBtn.clicked.connect()??????????????????????????????????????
        members = QTextEdit()
        vbox2.addWidget(QLabel("Members"))
        vbox2.addWidget(members)
        vbox2.addWidget(inviteBtn)

        hbox2 = QHBoxLayout()
        hbox2.addLayout(vbox1)
        hbox2.addLayout(vbox2)

        self.setLayout(hbox2)