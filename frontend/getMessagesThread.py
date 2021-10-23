__author__ = 'Osama Kashif'
__version__ = '1.0.0'

from PyQt5.QtCore import QThread, pyqtSignal

class GetMessagesThread(QThread):
    messages = pyqtSignal(list)

    def __init__(self, client):
        super().__init__()
        self.Finding = True
        self.client = client
    
    def run(self):
        while self.Finding:
            data = self.client.receiveData()
            if data[1] != data[2]:
                self.messages.emit(data)
    
    def stop(self):
        self.Finding = False

    def restart(self):
        self.Finding = True