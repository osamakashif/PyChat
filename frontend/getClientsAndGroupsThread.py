__author__ = 'Osama Kashif'
__version__ = '1.0.0'

from PyQt5.QtCore import QThread, pyqtSignal

class GetClientsAndGroupsThread(QThread):
    allClientsAndGroups = pyqtSignal(list)

    def __init__(self, client):
        super().__init__()
        self.Finding = True
        self.client = client
    
    def run(self):
        while self.Finding:
            data = self.client.getAllClientsAndGroups()
            self.allClientsAndGroups.emit(data)
    
    def stop(self):
        self.Finding = False

    def restart(self):
        self.Finding = True