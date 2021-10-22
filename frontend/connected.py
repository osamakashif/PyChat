__author__ = 'Osama Kashif'
__version__ = '1.0.0'

from PyQt5.QtWidgets import (QWidget, QMessageBox, QLabel,
                             QPushButton, QHBoxLayout, QVBoxLayout, QLabel, QListWidget)
from PyQt5.QtCore import QCoreApplication
from backend.group import Group
from frontend.clientToClient import ClientToClient
from frontend.getClients import GetClientThread
from frontend.getGroups import GetGroupsThread
from frontend.groupChat import GroupChat
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


        
        # self.createThread = CreateGroupThread(self.client)
        # self.clientThread.allClients.connect(self.addClientsToListDynamically)
        createBtn = QPushButton('Create', self)
        createBtn.resize(createBtn.sizeHint())
        # createBtn.clicked.connect(self.createThread.start)
        createBtn.clicked.connect(self.createGroup)

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
        self.clientsList = self.client.getAllClients()
        # print(allClients)
        self.connectedClients = QListWidget()
        self.clientThread = GetClientThread(self.client)
        self.clientThread.allClients.connect(self.addClientsToListDynamically)
        self.clientThread.start()
        # Send request for list of clientsself.findClientsThread = FindClientsThread(self.client)
        # self.findClientsThread.clients.connect(self.updateServerInfo)
        # self.findClientsThread.invite.connect(self.updateServerInfo)
        # self.findClientsThread.start()

        # for (ip, port, cname), clientData in allClients.items():
        #     if ((cname == self.client.name) & (ip == self.client.addr.replace("'","")) & (port == self.client.portAddr)):
        #         connectedClients.addItem(self.client.name + " (me)")
        #     else:
        #         connectedClients.addItem(cname)
        # selectedClientIndex = connectedClients.currentIndex()
        # print(selectedClientIndex)
        self.selectedClientIndex = self.connectedClients.currentRow()
        # selectedClientIndex = 0
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
        # self.groupsList = self.client.getAllGroups()
        # self.groupThread = GetGroupsThread(self.client)
        # self.groupThread.allGroups.connect(self.addGroupsToListDynamically)
        # self.groupThread.start()
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

    def addClientsToListDynamically(self, allClients):
        self.clientsList = allClients
        self.selectedClientIndex = self.connectedClients.currentRow()
        for (ip, port, cname), clientData in allClients.items():
            # print(ip, port, cname)
            if ((cname == self.client.name) & (ip == self.client.addr.replace("'", "")) & (port == self.client.portAddr)):
                toAdd = cname + " (me)"
                there = False
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
    
    def addGroupsToListDynamically(self, allGroups):
        self.clientsList = allGroups
        self.selectedClientIndex = self.groupChats.currentRow()
        for (ip, port, cname), groupData in allGroups.items():
            for val in groupData:
                toAdd = "Room " + str(val) + " by " + cname
                there = False
                for i in range(self.groupChats.count()):
                    if toAdd == self.groupChats.item(i).text():
                        there = True
                if (not there):
                    self.groupChats.addItem(toAdd)
            # if ((cname == self.client.name) & (ip == self.client.addr.replace("'", "")) & (port == self.client.portAddr)):
            #     toAdd = cname + " (me)"
            #     there = False
            #     for i in range(self.connectedClients.count()):
            #         if toAdd == self.connectedClients.item(i).text():
            #             there = True
            #     if (not there):
            #         self.connectedClients.addItem(toAdd)
            # else:
            #     toAdd = cname
            #     there = False
            #     for i in range(self.connectedClients.count()):
            #         if toAdd == self.connectedClients.item(i).text():
            #             there = True
            #     if (not there):
            #         self.connectedClients.addItem(toAdd)

    def close(self):
        self.clientThread.stop()
        # self.groupThread.stop()
        time.sleep(0.5)
        self.client.cleanup()
        self.hide()
        self.connection.show()

    def toC2C(self, client):
        self.clientThread.stop()
        # self.groupThread.stop()
        time.sleep(0.5)
        self.c2c = ClientToClient(client, self)
        self.hide()
        self.c2c.show()

    def createGroup(self):
        self.clientThread.stop()
        # self.groupThread.stop()
        # time.sleep(0.5)
        self.client.createGroup()
        group = Group(1, self.client.name)
        self.gc = GroupChat(group)
        self.hide()
        self.gc.show()
        # Group(1,"Room", self.client) #Need to change 1 to be dynamic ---?????????????????????????

    def toGChat(self, group):
        self.clientThread.stop()
        # self.groupThread.stop()
        time.sleep(0.5)
        self.gc = GroupChat(group)
        self.hide()
        self.gc.show()
