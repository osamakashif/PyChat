__author__ = 'Osama Kashif'
__version__ = '1.0.0'

from PyQt5.QtWidgets import (QListWidget, QWidget, QLineEdit, QLabel, QPushButton, QHBoxLayout, QVBoxLayout, QTextEdit, QLabel)
from frontend.getGroupChatThread import GetGroupChatThread
from frontend.inviteToGroup import InviteToGroup
from datetime import datetime

class GroupChat(QWidget):     
    
    def __init__(self, client, id, previousScreen, thread):
        super().__init__()
        self.initUI(client, id, previousScreen, thread)

    def initUI(self, client, id, previousScreen, thread):

        self.client = client
        self.connected = previousScreen
        self.id = id
        self.getClientsAndGroupsThread = thread
        
        sendBtn = QPushButton('Send', self)
        sendBtn.resize(sendBtn.sizeHint())
        sendBtn.clicked.connect(self.sendMsg)

        closeBtn = QPushButton('Close', self)
        closeBtn.resize(closeBtn.sizeHint())
        closeBtn.clicked.connect(self.close)
        
        self.sendBox = QLineEdit()
        self.hostIP = ""
        self.hostPort = ""
        self.hostName = ""

        hbox1 = QHBoxLayout()
        hbox1.addWidget(self.sendBox)
        hbox1.addWidget(sendBtn)
        vbox1 = QVBoxLayout()
        self.chatHistory = QTextEdit()
        self.groupChatLabel = QLabel("Room " + str(self.id) + " by " + self.hostName)
        vbox1.addWidget(self.groupChatLabel)
        vbox1.addWidget(self.chatHistory)
        vbox1.addLayout(hbox1)
        vbox1.addWidget(closeBtn)

        vbox2 = QVBoxLayout()
        inviteBtn = QPushButton('Invite', self)
        inviteBtn.resize(inviteBtn.sizeHint())
        inviteBtn.clicked.connect(self.toInvite)
        
        self.groupChatThread = GetGroupChatThread(self.client)
        self.groupChatThread.allClientsAndGroups.connect(self.addGroupMembersDynamically)
        self.groupChatThread.messages.connect(self.updateChatHistory)
        self.groupChatThread.start()

        self.inGroup = []
        self.members = QListWidget()
        vbox2.addWidget(QLabel("Members"))
        vbox2.addWidget(self.members)
        vbox2.addWidget(inviteBtn)

        hbox2 = QHBoxLayout()
        hbox2.addLayout(vbox1)
        hbox2.addLayout(vbox2)

        self.client.transmitForAllClientsAndGroups()

        self.setLayout(hbox2)

    def addGroupMembersDynamically(self, allClientsAndGroups):
        allClients = allClientsAndGroups[0]
        allGroups = allClientsAndGroups[1]
        for (ip, port, cname), groupData in allGroups.items():
            if self.id in groupData:
                self.hostIP = ip
                self.hostPort = port
                self.hostName = cname
                self.groupChatLabel.setText("Room " + str(self.id) + " by " + self.hostName)
                if (ip, port, cname) not in self.inGroup:
                    self.inGroup.append((ip, port, cname))
                    if ((cname == self.client.name) & (ip == self.client.addr.replace("'", "")) & (port == self.client.portAddr)):
                        self.members.addItem(cname + " (Host) (me)")
                    else:
                        self.members.addItem(cname + " (Host)")

        for (ip, port, cname), clientData in allClients.items():
            if (self.id in clientData):
                if (ip, port, cname) not in self.inGroup:
                    self.inGroup.append((ip, port, cname))
                    if ((cname == self.client.name) & (ip == self.client.addr.replace("'", "")) & (port == self.client.portAddr)):
                        self.members.addItem(cname + " (me)")
                    else:
                        self.members.addItem(cname)

    def updateChatHistory(self, messages):
        if messages[0] == 1:
            if messages[1] == self.id:
                self.chatHistory.append(str(messages[2][2]) + " (" + datetime.now().strftime("%H:%M") + ") : " + messages[3])

    def sendMsg(self):
        msg = self.sendBox.text()
        self.sendBox.clear()
        toSend = [1, self.id, (self.client.addr.replace("'", ""),self.client.portAddr,self.client.name), msg]
        self.chatHistory.append("Me (" + datetime.now().strftime("%H:%M") + ") : " + msg)
        self.client.sendMessage(toSend)
        self.client.transmitForAllClientsAndGroups()

    def toInvite(self):
        self.groupChatThread.stop()
        self.client.sendMessage([1,(self.client.addr.replace("'", ""),self.client.portAddr,self.client.name),(self.client.addr.replace("'", ""),self.client.portAddr,self.client.name),0])
        self.inviting = InviteToGroup(self.client, self.id, self, self.groupChatThread)
        self.hide()
        self.inviting.show()

    def close(self):
        self.groupChatThread.stop()
        self.client.sendMessage([1,(self.client.addr.replace("'", ""),self.client.portAddr,self.client.name),(self.client.addr.replace("'", ""),self.client.portAddr,self.client.name),0])
        self.hide()
        self.connected.show()
        self.getClientsAndGroupsThread.restart()
        self.getClientsAndGroupsThread.start()