import select
import socket
import sys
import signal
import argparse

from utils import *

SERVER_HOST = 'localhost'
# python server.py --name=server --port=9988
# python backend/server.py --name=server --port=9988

class ChatServer(object):
    """ An example chat server using select """

    def __init__(self, port, backlog=5):
        self.clients = 0
        self.clientmap = {}
        self.allClient = {}
        self.outputs = []  # list output sockets
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((SERVER_HOST, port))
        self.server.listen(backlog)
        # Catch keyboard interrupts
        signal.signal(signal.SIGINT, self.sighandler)

        print(f'Server (IP Address: {SERVER_HOST}) listening to port: {port} ...')

    def sighandler(self, signum, frame):
        """ Clean up client outputs"""
        print('Shutting down server...')

        # Close existing client sockets
        for output in self.outputs:
            output.close()

        self.server.close()

    def get_client_name(self, client):
        """ Return the name of the client """
        info = self.clientmap[client]
        host, name = info[0][0], info[1]
        return '@'.join((name, host))

    def run(self):
        # inputs = [self.server, sys.stdin]
        inputs = [self.server]
        self.outputs = []
        running = True
        while running:
            try:
                readable, writeable, exceptional = select.select(
                    inputs, self.outputs, [])
            except select.error as e:
                break

            for sock in readable:
                sys.stdout.flush()
                if sock == self.server:
                    # handle the server socket
                    client, address = self.server.accept()
                    print(
                        f'Chat server: got connection {client.fileno()} from {address}')
                    # Read the login name
                    cname = receive(client).split('NAME: ')[1]

                    # Compute client name and send back
                    self.clients += 1
                    send(client, f'CLIENT: {str(address)}')
                    inputs.append(client)

                    self.clientmap[client] = (address, cname)
                    self.allClient[(address[0], address[1], cname)] = {}
                    # Send joining information to other clients
                    # msg = f'\n(Connected: New client ({self.clients}) from {self.get_client_name(client)})'
                    # for output in self.outputs:
                    #     send(output, msg)
                    self.outputs.append(client)

                # elif sock == sys.stdin:
                #     # didn't test sys.stdin on windows system
                #     # handle standard input
                #     cmd = sys.stdin.readline().strip()
                #     if cmd == 'list':
                #         print(self.clientmap.values())
                #     elif cmd == 'quit':
                #         running = False
                else:
                    # handle all other sockets
                    try:
                        data = receive(sock)
                        if data:
                            if type(data) == bool:
                                if (data == True):
                                    client = self.get_client_name(sock)
                                    client = client.rpartition('@')[0]
                                    # print("Sending a list of clients to '"+self.get_client_name(sock)+"'") 
                                    send_clients(self.allClient, sock)
                            else:
                                # Send as new client's message...
                                msg = f'\n#[{self.get_client_name(sock)}]>> {data}'

                                # Send data to all except ourself
                                for output in self.outputs:
                                    if output != sock:
                                        send(output, msg)
                        else:
                            print(f'Chat server: {sock.fileno()} hung up')
                            self.clients -= 1
                            sock.close()
                            inputs.remove(sock)
                            self.outputs.remove(sock)

                            # Sending client leaving information to others
                            # msg = f'\n(Now hung up: Client from {self.get_client_name(sock)})'

                            # for output in self.outputs:
                            #     send(output, msg)
                    except socket.error as e:
                        # Remove
                        inputs.remove(sock)
                        self.outputs.remove(sock)

        self.server.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Socket Server Example with Select')
    parser.add_argument('--name', action="store", dest="name", required=True)
    parser.add_argument('--port', action="store",
                        dest="port", type=int, required=True)
    given_args = parser.parse_args()
    port = given_args.port
    name = given_args.name

    server = ChatServer(port)
    server.run()
