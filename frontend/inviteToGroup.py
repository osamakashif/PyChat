__author__ = 'Osama Kashif'
__version__ = '1.0.0'

from PyQt5.QtWidgets import (QWidget, QLineEdit, QLabel, QPushButton, QHBoxLayout, QVBoxLayout, QLabel, QListWidget)
from frontend.getClientsAndGroupsThread import GetClientsAndGroupsThread

class InviteToGroup(QWidget):     
    
    def __init__(self, client, id, previousScreen, thread):
        super().__init__()
        self.initUI(client, id, previousScreen, thread)

    def initUI(self, client, id, previousScreen, thread):

        self.groupChat = previousScreen
        self.client = client
        self.id = id
        self.groupChatThread = thread

        inviteBtn = QPushButton('Invite', self)
        inviteBtn.resize(inviteBtn.sizeHint())
        inviteBtn.clicked.connect(self.invite)

        cancelBtn = QPushButton('Cancel', self)
        cancelBtn.resize(cancelBtn.sizeHint())
        cancelBtn.clicked.connect(self.close)
        
        self.remainingClients = []
        self.clientAndGroupsThread = GetClientsAndGroupsThread(self.client)
        self.clientAndGroupsThread.allClientsAndGroups.connect(self.showConnectedClientsNotInGroup)
        self.clientAndGroupsThread.start()


        hbox = QHBoxLayout()
        hbox.addWidget(inviteBtn)
        hbox.addWidget(cancelBtn)
        vbox = QVBoxLayout()
        self.otherClients = QListWidget()
        self.selectedClientIndex = self.otherClients.currentRow()
        vbox.addWidget(QLabel("Connected Clients"))
        vbox.addWidget(self.otherClients)
        vbox.addLayout(hbox)

        self.setLayout(vbox)

    def showConnectedClientsNotInGroup(self, allClientsAndGroups):
        allClients = allClientsAndGroups[0]
        self.selectedClientIndex = self.otherClients.currentRow()
        for (ip, port, cname), clientData in allClients.items():
            if (self.id not in clientData):
                if (ip, port, cname) not in self.remainingClients:
                    self.remainingClients.append((ip, port, cname))
                    self.otherClients.addItem(cname)

    def invite(self):
        self.clientAndGroupsThread.stop()
        selected = self.remainingClients[self.selectedClientIndex]
        self.client.sendMessage([4, selected, self.id, "work"])
        self.clientAndGroupsThread.restart()
        self.clientAndGroupsThread.start()

    def close(self):
        self.clientAndGroupsThread.stop()
        self.hide()
        self.groupChat.show()
        self.groupChatThread.restart()
        self.groupChatThread.start()
        self.client.transmitForAllClientsAndGroups()