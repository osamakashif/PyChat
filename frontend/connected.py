__author__ = 'Osama Kashif'
__version__ = '1.0.0'

from PyQt5.QtWidgets import (QWidget, QMessageBox, QLabel, QPushButton, QHBoxLayout, QVBoxLayout, QLabel, QListWidget)
from frontend.clientToClient import ClientToClient
from frontend.groupChat import GroupChat
from frontend.getClientsAndGroupsThread import GetClientsAndGroupsThread
import time


class Connected(QWidget):

    def __init__(self, client, previousScreen):
        super().__init__()
        self.initUI(client, previousScreen)

    def initUI(self, client, previousScreen):

        self.client = client
        self.connection = previousScreen
        chat1_1Btn = QPushButton('1:1 Chat', self)
        chat1_1Btn.resize(chat1_1Btn.sizeHint())

        createBtn = QPushButton('Create', self)
        createBtn.resize(createBtn.sizeHint())
        createBtn.clicked.connect(self.createGroup)

        joinBtn = QPushButton('Join', self)
        joinBtn.resize(joinBtn.sizeHint())
        joinBtn.clicked.connect(self.toGChat)

        closeBtn = QPushButton('Close', self)
        closeBtn.resize(closeBtn.sizeHint())
        closeBtn.clicked.connect(self.close)

        hbox1 = QHBoxLayout()
        self.clientsList = self.client.getAllClientsAndGroups()
        self.connectedClients = QListWidget()
        self.clientAndGroupsThread = GetClientsAndGroupsThread(self.client)
        self.clientAndGroupsThread.allClientsAndGroups.connect(self.addClientsAndGroupsToListDynamically)
        self.clientAndGroupsThread.start()
        self.groupsForClient = []
        self.selectedClientIndex = self.connectedClients.currentRow()
        chat1_1Btn.clicked.connect(lambda: self.toC2C(list(self.clientsList.items())[self.selectedClientIndex]))
        hbox1.addWidget(self.connectedClients)
        hbox1.addWidget(chat1_1Btn)

        vbox1 = QVBoxLayout()
        vbox1.addWidget(QLabel('Connected Clients'))
        vbox1.addLayout(hbox1)

        vbox2 = QVBoxLayout()
        vbox2.addWidget(createBtn)
        vbox2.addWidget(joinBtn)

        hbox2 = QHBoxLayout()
        self.groupChats = QListWidget()
        self.selectedGroupIndex = self.groupChats.currentRow()
        hbox2.addWidget(self.groupChats)
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

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def addClientsAndGroupsToListDynamically(self, allClientsAndGroups):
        allClients = allClientsAndGroups[0]
        allGroups = allClientsAndGroups[1]
        
        self.clientsList = allClients
        self.selectedClientIndex = self.connectedClients.currentRow()
        self.selectedGroupIndex = self.groupChats.currentRow()
        for (ip, port, cname), clientData in allClients.items():
            if ((cname == self.client.name) & (ip == self.client.addr.replace("'", "")) & (port == self.client.portAddr)):
                toAdd = cname + " (me)"
                there = False
                for val in clientData:
                    if val not in self.groupsForClient:
                        self.groupsForClient.append(val)
                for i in range(self.connectedClients.count()):
                    if toAdd == self.connectedClients.item(i).text():
                        there = True
                if (not there):
                    self.connectedClients.addItem(toAdd)
            else:
                toAdd = cname
                there = False
                for i in range(self.connectedClients.count()):
                    if toAdd == self.connectedClients.item(i).text():
                        there = True
                if (not there):
                    self.connectedClients.addItem(toAdd)
        for (ip, port, cname), groupData in allGroups.items():
            for val in groupData:
                if val in self.groupsForClient:
                    toAdd = "Room " + str(val) + " by " + cname
                    there = False
                    for i in range(self.groupChats.count()):
                        if toAdd == self.groupChats.item(i).text():
                            there = True
                    if (not there):
                        self.groupChats.addItem(toAdd)

    def close(self):
        self.clientAndGroupsThread.stop()
        time.sleep(0.5)
        self.client.cleanup()
        self.hide()
        self.connection.show()

    def toC2C(self, client):
        self.clientAndGroupsThread.stop()
        time.sleep(0.5)
        self.c2c = ClientToClient(self.client, client, self, self.clientAndGroupsThread)
        self.hide()
        self.c2c.show()

    def createGroup(self):
        self.clientAndGroupsThread.stop()
        time.sleep(0.5)
        self.client.createGroup()
        self.clientAndGroupsThread.restart()
        self.clientAndGroupsThread.start()
    

    def toGChat(self):
        self.clientAndGroupsThread.stop()
        time.sleep(0.5)
        self.gc = GroupChat(self.client, self.groupsForClient[self.selectedGroupIndex], self, self.clientAndGroupsThread)
        self.hide()
        self.gc.show()
