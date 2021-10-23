__author__ = 'Osama Kashif'
__version__ = '1.0.0'

from PyQt5.QtCore import QThread, pyqtSignal

class GetGroupChatThread(QThread):
    allClientsAndGroups = pyqtSignal(list)
    messages = pyqtSignal(list)

    def __init__(self, client):
        super().__init__()
        self.Finding = True
        self.client = client
    
    def run(self):
        while self.Finding:
            # self.client.transmitForAllClientsAndGroups()
            data = self.client.receiveData()
            if type(data[0]) == int:
                if data[1] != data[2]:
                    self.messages.emit(data)
                else:
                    self.Finding = False
            else:
                self.allClientsAndGroups.emit(data)
            # clientData = self.client.getAllClientsAndGroups()
            # self.allClientsAndGroups.emit(clientData)
            # data = self.client.receiveData()
            # print(data)
            # if type(data[0]) == int:
            #     if data[1] != data[2]:
            #         self.messages.emit(data)
    
    def stop(self):
        self.Finding = False

    def restart(self):
        self.Finding = True