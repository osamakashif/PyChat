__author__ = 'Osama Kashif'
__version__ = '1.0.0'

from PyQt5.QtWidgets import (QWidget, QLineEdit, QLabel, QPushButton, QHBoxLayout, QVBoxLayout, QLabel, QListWidget)

class InviteToGroup(QWidget):     
    
    def __init__(self, client):
        super().__init__()
        self.initUI(client)

    def initUI(self, client):

        inviteBtn = QPushButton('Invite', self)
        inviteBtn.resize(inviteBtn.sizeHint())
        # inviteBtn.clicked.connect()??????????????????????????????????????

        cancelBtn = QPushButton('Cancel', self)
        cancelBtn.resize(cancelBtn.sizeHint())
        # closeBtn.clicked.connect()??????????????????????????????????????
        
        # self.sendBox = QLineEdit()

        hbox = QHBoxLayout()
        hbox.addWidget(inviteBtn)
        hbox.addWidget(cancelBtn)
        vbox = QVBoxLayout()
        otherClients = QListWidget()
        vbox.addWidget(QLabel("Connected Clients"))
        vbox.addWidget(otherClients)
        vbox.addWidget(hbox)

        self.setLayout(vbox)