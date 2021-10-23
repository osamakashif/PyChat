__author__ = 'Osama Kashif'
__version__ = '1.0.0'

from PyQt5.QtWidgets import (QWidget, QLineEdit, QLabel, QPushButton, QHBoxLayout, QVBoxLayout, QTextEdit, QLabel)

from backend.utils import send
from frontend.getMessagesThread import GetMessagesThread
from datetime import datetime

class ClientToClient(QWidget):     
    
    def __init__(self, client, clientToTalkTo, previousScreen, thread):
        super().__init__()
        self.initUI(client, clientToTalkTo, previousScreen, thread)

    def initUI(self, client, clientToTalkTo, previousScreen, thread):
        self.connected = previousScreen
        self.client = client
        self.clientToTalkTo = clientToTalkTo
        self.getClientsAndGroupsThread = thread
        sendBtn = QPushButton('Send', self)
        sendBtn.resize(sendBtn.sizeHint())
        sendBtn.clicked.connect(self.sendMsg)

        closeBtn = QPushButton('Close', self)
        closeBtn.resize(closeBtn.sizeHint())
        closeBtn.clicked.connect(self.close)
        
        self.sendBox = QLineEdit()

        self.messageThread = GetMessagesThread(self.client)
        self.messageThread.messages.connect(self.updateChatHistory)
        self.messageThread.start()

        hbox = QHBoxLayout()
        hbox.addWidget(self.sendBox)
        hbox.addWidget(sendBtn)
        vbox = QVBoxLayout()
        self.chatHistory = QTextEdit()
        vbox.addWidget(QLabel("Chat with "+ str(self.clientToTalkTo[0][2])))
        vbox.addWidget(self.chatHistory)
        vbox.addLayout(hbox)
        vbox.addWidget(closeBtn)

        self.setLayout(vbox)

    def updateChatHistory(self, messages):
        if messages[0] == 0:
            if messages[1] == (self.client.addr.replace("'", ""),self.client.portAddr,self.client.name):
                if messages[2] == self.clientToTalkTo[0]:
                    self.chatHistory.append(str(self.clientToTalkTo[0][2]) + " (" + datetime.now().strftime("%H:%M") + ") : " + messages[3])

    def sendMsg(self):
        msg = self.sendBox.text()
        self.sendBox.clear()
        toSend = [0, self.clientToTalkTo[0], (self.client.addr.replace("'", ""),self.client.portAddr,self.client.name), msg]
        self.chatHistory.append("Me (" + datetime.now().strftime("%H:%M") + ") : " + msg)
        self.client.sendMessage(toSend)

    def close(self):
        self.client.sendMessage([0,(self.client.addr.replace("'", ""),self.client.portAddr,self.client.name),(self.client.addr.replace("'", ""),self.client.portAddr,self.client.name),0])
        self.messageThread.stop()
        self.hide()
        self.connected.show()
        self.getClientsAndGroupsThread.restart()
        self.getClientsAndGroupsThread.start()