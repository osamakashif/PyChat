import select
import socket
import sys
import signal
import argparse
import threading

# from utils import *
# from utils import *
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
        
        # Connect to server at port
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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
        """Close the connection and wait for the thread to terminate."""
        self.sock.close()
    
    def getAllClients(self):
        send(self.sock, True)
        data = receive(self.sock)
        return data

    def run(self):
        """ Chat client main loop """
        while self.connected:
            try:
                sys.stdout.write(self.prompt)
                sys.stdout.flush()

                # Wait for input from stdin and socket
                # readable, writeable, exceptional = select.select([0, self.sock], [], [])
                readable, writeable, exceptional = select.select(
                    [self.sock], [], [])

                for sock in readable:
                    # if sock == 0:
                    #     data = sys.stdin.readline().strip()
                    #     if data:
                    #         send(self.sock, data)
                    if sock == self.sock:
                        data = receive(self.sock)
                        if type(data) == list:
                            data = receive_clients(data, self.name)
                        if not data:
                            print('Client shutting down.')
                            self.connected = False
                            break
                        else:
                            sys.stdout.write(data + '\n')
                            sys.stdout.flush()

            except KeyboardInterrupt:
                print(" Client interrupted. " "")
                stop_thread = True
                self.cleanup()
                break


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
