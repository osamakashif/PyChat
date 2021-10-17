__author__ = 'Osama Kashif'
__version__ = '1.0.0'

from PyQt5.QtWidgets import (QWidget, QMessageBox, QLabel, QPushButton, QHBoxLayout, QVBoxLayout, QLabel, QListWidget)
from PyQt5.QtCore import QCoreApplication
from backend.group import Group
from frontend.clientToClient import ClientToClient
from frontend.groupChat import GroupChat

class Connected(QWidget):     
    
    def __init__(self, client):
        super().__init__()
        self.initUI(client)

    def initUI(self, client):
        
        self.client = client

        chat1_1Btn = QPushButton('1:1 Chat', self)
        chat1_1Btn.resize(chat1_1Btn.sizeHint())

        createBtn = QPushButton('Create', self)
        createBtn.resize(createBtn.sizeHint())

        joinBtn = QPushButton('Join', self)
        joinBtn.resize(joinBtn.sizeHint())

        closeBtn = QPushButton('Close', self)
        closeBtn.resize(closeBtn.sizeHint())
        # def close():
        #     QCoreApplication.instance().quit()
            # threading.Thread(target=client.cleanup).start()
        closeBtn.clicked.connect(self.close)
        # closeBtn.pressed(client.cleanup)

        hbox1 = QHBoxLayout()
        allClients = self.client.getAllClients()
        # print(allClients)
        connectedClients = QListWidget()
        for (ip, port, cname), clientData in allClients.items():
            if ((cname == self.client.name) & (ip == self.client.addr.replace("'","")) & (port == self.client.portAddr)):
                connectedClients.addItem(self.client.name + " (me)")
            else:
                connectedClients.addItem(cname)
        # selectedClientIndex = connectedClients.currentIndex()
        # print(selectedClientIndex)
        selectedClientIndex = connectedClients.currentRow()
        # selectedClientIndex = 0
        chat1_1Btn.clicked.connect(lambda: self.toC2C(list(allClients.items())[selectedClientIndex]))
        hbox1.addWidget(connectedClients)
        hbox1.addWidget(chat1_1Btn)

        vbox1 = QVBoxLayout()
        vbox1.addWidget(QLabel('Connected Clients'))
        vbox1.addLayout(hbox1)

        vbox2 = QVBoxLayout()
        vbox2.addWidget(createBtn)
        vbox2.addWidget(joinBtn)

        hbox2 = QHBoxLayout()
        groupChats = QListWidget()
        hbox2.addWidget(groupChats)
        hbox2.addLayout(vbox2)

        vbox3 = QVBoxLayout()
        vbox3.addWidget(QLabel('Chat Rooms (Group Chat)'))
        vbox3.addLayout(hbox2)

        hbox3 = QHBoxLayout()
        hbox3.addStretch(3)
        hbox3.addWidget(closeBtn)

        vbox = QVBoxLayout()
        vbox.addLayout(vbox1)
        vbox.addLayout(vbox3)
        vbox.addLayout(hbox3)

        self.setLayout(vbox)
    
    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message', 'Are you sure to quit?',
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:        event.accept()
        else:                               event.ignore()

    def close(self):
        self.client.cleanup()
        self.hide()
        # self.show()

    def toC2C(self, client):
        self.c2c = ClientToClient(client=client)
        self.hide()
        self.c2c.show()

    def toGChat(self, group):
        gc = GroupChat(group=group)
