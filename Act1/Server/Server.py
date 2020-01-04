from datetime import datetime
from concurrent import futures
import logging
import socket

import grpc

import act1.Act1_pb2 as Act1_pb2
import act1.Act1_pb2_grpc as Act1_pb2_grpc

class Chat(Act1_pb2_grpc.ChatServicer):

    def HandShake(self, request, context):
        global users

        name = request.Username
        if name in users:
            m = "Welcome back %s!" % name
        else:
            m = "Welcome %s! Thanks for choosing us" % name
            users.add(name)

        return Act1_pb2.basicMsg(From = "server",
                                  Msg = m)

    def Dispatch(self, request, context):
        global lastID
        
        with open("log.txt", "a") as log:
            lastID += 1
            msg = "%i;%s;%s;%s;%s\n" % (lastID, 
                                      request.From, 
                                      request.To, 
                                      request.Msg, 
                                      request.Date)
            log.write(msg)

        return Act1_pb2.basicMsg(From = "server", 
                                  Msg = "msgSent")

    #rpc Retrieve(basicMsg) returns (stream FullMsg) {}
    def Retrieve(self, request, context):

        wo = request.From
        with open("log.txt", "r") as log:
            for line in log:
                l = line.split(";")
                if wo == l[2]:
                    yield Act1_pb2.FullMsg(From = l[1].strip(),
                                            To = wo,
                                            Msg = l[3].strip(),
                                            Date = l[4].strip())
        yield Act1_pb2.FullMsg(From = "server",
                                To = wo,
                                Msg = "No More Msgs",
                                Date = datetime.now().strftime("%b-%d-%Y %H:%M:%S"))

class Clients(Act1_pb2_grpc.ClientsServicer):
    
    #rpc GetClients (basicMsg) returns (stream Act1Request) {}
    def GetClients(self, request, context):
        global users

        wo = request.From
        for i in users:
            yield Act1_pb2.Act1Request(Username = i)

class GetAll(Act1_pb2_grpc.GetAllServicer):
    
    #rpc GetAllSent (basicMsg) returns (stream FullMsg) {}
    def GetAllSent(self, request, context):
        wo = request.From

        with open("log.txt", "r") as log:
            for line in log:
                l = line.split(";")
                if wo == l[1]:
                    yield Act1_pb2.FullMsg(From = wo,
                                            To = l[2].strip(),
                                            Msg = l[3].strip(),
                                            Date = l[4].strip())
        yield Act1_pb2.FullMsg(From = "server",
                                To = wo,
                                Msg = "No More Msgs",
                                Date = datetime.now().strftime("%b-%d-%Y %H:%M:%S"))

def getUsers():
    global users
    global lastID

    #ID;from;to;msg;date
    with open("log.txt", "r") as log:
        for line in log:
            l = line.split(";")
            users.add(l[1])
            users.add(l[2])
            lastID += 1
    return users

def getIP():
    try:
        success = True
        host_name = socket.gethostname() 
        host_ip = socket.gethostbyname(host_name)
    except:
        success = False
        print("Unable to get IP")
    return host_ip if success else "0"

def serve():
    global users

    #First get the currents users.
    users = getUsers()

    #Second, set the Server settings
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    #add the chat class
    Act1_pb2_grpc.add_ChatServicer_to_server(Chat(), server)
    #add the Clients class
    Act1_pb2_grpc.add_ClientsServicer_to_server(Clients(), server)
    #add the GetAll class
    Act1_pb2_grpc.add_GetAllServicer_to_server(GetAll(), server)

    server.add_insecure_port('[::]:50051')

    print("Server Running on %s" % getIP())

    server.start()
    server.wait_for_termination()

users = set()
lastID = 0
if __name__ == '__main__':
    logging.basicConfig()
    serve()