from datetime import datetime
import time

time.sleep(180)

PATH = ""

import pika

#The messages the server will receive have the following structure:
#     0  ;  1 ; 2;   3   ;  4 ;  5 ;  6
# Service;From;To;Message;Date;Next;Other?
# Service is a number between 0 and 2 where:
#  - 0 is the Chat service
#  - 1 is the Clients service
#  - 2 is the GetAll service
# From and To are the names of the users or clients
# Message is the name of method required or the message that want to be sent itself
# Date is the date
# Next is a flag used to notice that the server/client should wait the "next" message before doing something.
# Other? is any other thing that might be appended to the message

#Note that depending on the service-method needed, some parameters of the message may not be used or filed.

#Inside the server, each class will represent a service of it

class Chat(object):

    def HandShake(self, ch, method, props, body, server):

        users = set(server.getUsers())

        msg = str(body)
        name = (msg.split(";"))[1]

        if name in users:
            m = "Welcome back %s!" % name
        else:
            m = "Welcome %s! Thanks for choosing us" % name
            server.addUser(name)

        toSend = "0;server;%s;%s;date;0; " % (name, m)
        server.send(ch, method, props, body, toSend, 0)

    def Dispatch(self, ch, method, props, body, server):
        
        lastID = int(server.getLastID())
        msg = str(body)
        msg = msg.split(";")
        name = msg[1]
        
        with open(PATH+"log.txt", "a") as log:
            m = "%i;%s;%s;%s;%s\n" % (lastID, 
                                      name, 
                                      msg[2], 
                                      msg[3], 
                                      msg[4])
            log.write(m)
            server.increaseLastID()

        m = "msgSent"
        toSend = "0;server;%s;%s;date;0; " % (name, m)
        server.send(ch, method, props, body, toSend, 0)


    #rpc Retrieve(basicMsg) returns (stream FullMsg) {}
    def Retrieve(self, ch, method, props, body, server):

        msg = str(body)
        wo = (msg.split(";"))[1]

        with open(PATH+"log.txt", "r") as log:
            for line in log:
                l = line.split(";")
                l = list(map(str.strip, l))
                #print(l)
                if wo == l[2]:
                    toSend = "0;%s;%s;%s;%s;1; " % (l[1], wo, l[3], l[4])
                    server.send(ch, method, props, body, toSend, 1)
                    time.sleep(0.1)

        date = datetime.now().strftime("%b-%d-%Y %H:%M:%S")
        toSend = toSend = "0;server;%s;No More Msgs;%s;0; " % (wo, date)
        server.send(ch, method, props, body, toSend, 0)

class Clients(object):
    
    #rpc GetClients (basicMsg) returns (stream Act1Request) {}
    def GetClients(self, ch, method, props, body, server):
        
        users = set(server.getUsers())

        msg = str(body)
        wo = (msg.split(";"))[1]

        while len(users) > 1:
            currUsr = users.pop()
            toSend = "1;server;%s;%s;date;1; " % (wo, currUsr)
            server.send(ch, method, props, body, toSend, 1)
            time.sleep(0.1)

        currUsr = users.pop()
        toSend = "1;server;%s;%s;date;0; " % (wo, currUsr)
        server.send(ch, method, props, body, toSend, 0)

class GetAll(object):
    
    #rpc GetAllSent (basicMsg) returns (stream FullMsg) {}
    def GetAllSent(self, ch, method, props, body, server):

        msg = str(body)
        wo = (msg.split(";"))[1]

        with open(PATH+"log.txt", "r") as log:
            for line in log:
                l = line.split(";")
                l = list(map(str.strip, l))
                if wo == l[1]:
                    toSend = "2;%s;%s;%s;%s;1; " % (wo, l[2], l[3], l[4])
                    server.send(ch, method, props, body, toSend, 1)
                    time.sleep(0.1)

        date = datetime.now().strftime("%b-%d-%Y %H:%M:%S")
        toSend = toSend = "2;server;%s;No More Msgs;%s;0; " % (wo, date)
        server.send(ch, method, props, body, toSend, 0)

class Server(object):

    users = set()
    lastID = 0

    def __init__(self):
        
        print(" [x] Initializing server...")

        #First get the currents users.
        self.getUsersInit()

        #Second we set the connection with the pika service.
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='rabbit'))

        #Creating the channel
        self.channel = self.connection.channel()

        #Creating the queue to receive msgs
        self.channel.queue_declare(queue='server_queue')

        self.channel.basic_consume(
            queue='server_queue', 
            on_message_callback=self.messageHandler)

        self.Service_Chat = Chat()
        self.Service_Clients = Clients()
        self.Service_GetAll = GetAll()

        print(" [x] Server initialized and ready to start")

    def initServer(self):
        print(" [x] Awaiting for new messages ")
        self.channel.start_consuming()

    def messageHandler(self, ch, method, props, body):
        
        print("[*] Handling the request")

        msg = str(body)
        msg = msg.split(";")
        msg[0] = msg[0][2]
        name = msg[1]

        print(msg)

        if msg[0] == "0":
            if msg[3] == "HandShake":
                self.Service_Chat.HandShake(ch, method, props, body, self)
            elif msg[3] == "Retrieve":
                self.Service_Chat.Retrieve(ch, method, props, body, self)
            else:
                self.Service_Chat.Dispatch(ch, method, props, body, self)
        elif msg[0] == "1":
            if msg[3] == "GetClients":
                self.Service_Clients.GetClients(ch, method, props, body, self)
            else:
                m = "The Method doesn't exist in the server, please check the name and/or number."
                toSend = "error;server;%s;%s;date;0; " % (name, m)
                self.send(ch, method, props, body, toSend, 0)
        elif msg[0] == "2":
            if msg[3] == "GetAllSent":
                self.Service_GetAll.GetAllSent(ch, method, props, body, self)
            else:
                m = "The Method doesn't exist in the server, please check the name and/or number."
                toSend = "error;server;%s;%s;date;0; " % (name, m)
                self.send(ch, method, props, body, toSend, 0)
        # elif msg[0] == "9":
        #     print("outing")
        #     exit(0)
        else:
            m = "The service doesn't exist in the server, please check the number."
            toSend = "error;server;%s;%s;date;0; " % (name, m)
            self.send(ch, method, props, body, toSend, 0)

    def getUsersInit(self):
        #ID;from;to;msg;date
        with open(PATH+"log.txt", "r") as log:
            for line in log:
                l = line.split(";")
                self.users.add(l[1])
                self.users.add(l[2])
                self.lastID += 1
        return self.users

    def send(self, ch, method, props, body, toSend, next):
        ch.basic_publish(exchange = "", 
                        routing_key = props.reply_to,
                        properties = pika.BasicProperties(correlation_id = \
                                                                props.correlation_id),
                        body = str(toSend))
        if next != 1:
            ch.basic_ack(delivery_tag=method.delivery_tag)

    def getUsers(self):
        return self.users

    def addUser(self, usr):
        self.users.add(usr)

    def getLastID(self):
        return self.lastID

    def increaseLastID(self):
        self.lastID += 1

act2Server = Server()
act2Server.initServer()