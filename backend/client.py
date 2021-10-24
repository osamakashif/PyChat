__author__ = 'Osama Kashif'
__version__ = '1.0.0'

import socket
import sys
import argparse
import ssl

from backend.utils import send, receive, receive_clients

SERVER_HOST = 'localhost'

stop_thread = False

class ChatClient():
    """ A command line chat client using select """
    def __init__(self, name, port, host=SERVER_HOST):
        self.name = name
        self.connected = False
        self.host = host
        self.port = port
        self.addr = ""
        self.portAddr = 0

        self.context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        
        # Connect to server at port
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock = self.context.wrap_socket(self.sock, server_hostname=host)


            self.sock.connect((host, self.port))
            print(f'Now connected to chat server@ port {self.port}')
            self.connected = True
            
            # Send my name...
            send(self.sock, 'NAME: ' + self.name)
            data = receive(self.sock)
            
            # Contains client address, set it
            ipAndPort = data.split('CLIENT: ')[1][1:-1].split(", ")
            self.addr = ipAndPort[0]
            self.portAddr = int(ipAndPort[1])

        except socket.error as e:
            print(f'Failed to connect to chat server @ port {self.port}')
            sys.exit(1)

    def cleanup(self):
        send(self.sock, False)
        """Close the connection and wait for the thread to terminate."""
        self.sock.close()
    
    def getAllClientsAndGroups(self):
        send(self.sock, 2)
        data = receive(self.sock)
        return data

    def transmitForAllClientsAndGroups(self):
        send(self.sock, 2)


    def createGroup(self):
        send(self.sock, 3)

    def sendMessage(self, message):
        send(self.sock, message)
    
    def receiveData(self):
        data = receive(self.sock)
        return data


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--name', action="store", dest="name", required=True)
    parser.add_argument('--port', action="store",
                        dest="port", type=int, required=True)
    given_args = parser.parse_args()

    port = given_args.port
    name = given_args.name

    client = ChatClient(name=name, port=port)
    client.run()
