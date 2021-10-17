__author__ = 'Osama Kashif'
__version__ = '1.0.0'

class Group():

    def __init__(self, id, name, startingClient):
        self.id = id
        self.name = name
        self.host = startingClient
        self.startingClient = startingClient
        self.members = [startingClient]

    def addMember(self, client):
        self.members.append(client)

    def removeMember(self, client):
        self.members.remove(client)

    def getMembers(self):
        return self.members
    
    def getFullName(self):
        return (self.name + " by " + self.startingClient)

    # def getMemberNames(self):
    #     names = []
    #     for client in self.members:
    #         names.add(client.name)
    #     return self.members
