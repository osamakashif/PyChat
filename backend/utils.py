import socket
import pickle
import struct

def send(channel, *args):
    buffer = pickle.dumps(args)
    value = socket.htonl(len(buffer))
    size = struct.pack("L", value)
    channel.send(size)
    channel.send(buffer)

def receive(channel):
    size = struct.calcsize("L")
    size = channel.recv(size)
    try:
        size = socket.ntohl(struct.unpack("L", size)[0])
    except struct.error as e:
        return ''
    buf = ""
    while len(buf) < size:
        buf = channel.recv(size - len(buf))
    return pickle.loads(buf)[0]

# def send_clients(map, channel):
#     clients = []
#     for clientItem in map.items():
#         clients.append(clientItem)
#     send(channel, clients)

# def send_clients(map, channel):
#     clients = []
#     for clientItems, (address, name) in map.items():
#         clients.append((address, name))
#     send(channel, clients)

def send_clients(allClients, channel):
    send(channel, allClients)

def send_client_names(map, channel):
    clients = []
    for clientItems, (address, name) in map.items():
        clients.append(name)
    send(channel, clients)

def receive_clients(clientList, name):
    clientName = name
    clientAddress = ''
    clients = ""
    for address, cname in clientList:
        if (cname != name):
            if clients == "":
                clients = cname
            else:
                clients = f"{clients}, {cname}"
        else:
            clientAddress = address[0]
    msg = f'\n#[{clientName}@{clientAddress}]>> {clients}'
    return msg