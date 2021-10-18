__author__ = 'Osama Kashif'
__version__ = '1.0.0'

from PyQt5.QtCore import QThread, pyqtSignal

class GetClientThread(QThread):
    allClients = pyqtSignal(dict)

    def __init__(self, client):
        super().__init__()
        self.Finding = True
        self.client = client
    
    def run(self):
        while self.Finding:
            data = self.client.getAllClients()
            self.allClients.emit(data)
    
    def stop(self):
        self.Finding = False