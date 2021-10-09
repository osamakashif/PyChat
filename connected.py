__author__ = 'Osama Kashif'
__version__ = '1.0.0'

from PyQt5.QtWidgets import (QWidget, QMessageBox, QLabel, QPushButton, QHBoxLayout, QVBoxLayout, QTextEdit, QLabel)
from PyQt5.QtCore import QCoreApplication

class Connected(QWidget):     
    
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        chat1_1Btn = QPushButton('1:1 Chat', self)
        chat1_1Btn.resize(chat1_1Btn.sizeHint())

        createBtn = QPushButton('Create', self)
        createBtn.resize(createBtn.sizeHint())

        joinBtn = QPushButton('Join', self)
        joinBtn.resize(joinBtn.sizeHint())

        closeBtn = QPushButton('Close', self)
        closeBtn.resize(closeBtn.sizeHint())
        closeBtn.clicked.connect(QCoreApplication.instance().quit)

        hbox1 = QHBoxLayout()
        hbox1.addWidget(QTextEdit())
        hbox1.addWidget(chat1_1Btn)

        vbox1 = QVBoxLayout()
        vbox1.addWidget(QLabel('Connected Clients'))
        vbox1.addLayout(hbox1)

        vbox2 = QVBoxLayout()
        vbox2.addWidget(createBtn)
        vbox2.addWidget(joinBtn)

        hbox2 = QHBoxLayout()
        hbox2.addWidget(QTextEdit())
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