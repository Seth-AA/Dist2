from datetime import datetime
from random import choices, choice
import time

#time.sleep(180)

import pika
import uuid

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

ClientName = ""
#rabbit_1     | 2020-01-07 04:46:27.371 [info] <0.613.0> accepting AMQP connection <0.613.0> (172.31.52.178:53888 -> 172.31.60.146:5672)

def printMenu():
    print("\nWhat would you like to do?")
    print("1 - Write and Send a Message")
    print("2 - View received messages")
    print("3 - View sent messages")
    print("4 - View the full list of Clients of the server")
    print("0 - Logout")

def logIn(stub, cln = ""):
    global ClientName

    if cln == "":
        ClientName = input("Enter your Username: ")
    else:
        print("Enter your Username: %s" % cln)
        ClientName = cln

    toSend = "0;%s;server;HandShake;date;0; " % ClientName
    r = send(toSend)
    print(r[0][3])

def listClients(stub):
    global ClientName

    toSend = "%s;%s;server;GetClients;date;0; " % (stub, ClientName)
    r = send(toSend)

    i = 1
    print("The following is the list of current Clients in the Server: ")
    for l in r:
        print("%i - %s" % (i, l[3]))
        i += 1

def sendMsg(stub, dest = "", msg = ""):
    print("Indicate the username to which you want to send a message")
    if dest == "":
        dest = input("Username: ")
        msg = input("Message: ")
    else:
        print("Username: %s" % dest)
        print("Message: %s" % msg)
    date = datetime.now().strftime("%b-%d-%Y %H:%M:%S")

    toSend = "0;%s;%s;%s;%s;0; " % (ClientName, dest, msg, date)
    r = send(toSend)
    print(r[0][3])

def viewSentMsg(stub):

    toSend = "%s;%s;server;GetAllSent;date;0; " % (stub, ClientName)
    r = send(toSend)

    for msg in r:
        if msg[1] == "server":
            print(msg[3])
            break
        print("[%s] To: %s" % (msg[4], msg[2]))
        print("Message: %s" % msg[3])

def viewReceivedMsg(stub):

    toSend = "%s;%s;server;Retrieve;date;0; " % (stub, ClientName)
    r = send(toSend)

    for msg in r:
        if msg[1] == "server":
            print(msg[3])
            break
        print("[%s] From: %s" % (msg[4], msg[1]))
        print("Message: %s" % msg[3])

def myMain(stubChat, stubClients, stubGetAll):
    
    login = logIn(stubChat)
    
    while True:
        printMenu()

        opt = input("Your choice: ")
        print("")
        if opt == "1":
            sendMsg(stubChat)
        elif opt == "2":
            viewReceivedMsg(stubChat)
        elif opt == "3":
            viewSentMsg(stubGetAll)
        elif opt == "4":
            listClients(stubClients)
        elif opt == "0":
            break
        else:
            print("There is no such option, please choose one of the following options: ")

def simulation():
    tomoyo = ["UserX", "Hikari", "God", "Freund", "Darkness", "Death"]
    msgs = ["'sup dude?", "I'm fine", "How is your family?", "I love kittens", 
            "Love doggos LOL", "halp", "feels bad dude", "dead", "fine", "wanna chat?", "take me"]
    
    for i in range(4):

        login = logIn(stubChat, choice(tomoyo))

        while True:
            printMenu()

            opt = str(choices([0, 1, 2, 3, 4], [0.1, 0.3, 0.25, 0.25, 0.1])[0])
            print("Your choice: %s\n" % opt)
            if opt == "1":
                sendMsg(stubChat, choice(tomoyo), choice(msgs))
            elif opt == "2":
                viewReceivedMsg(stubChat)
            elif opt == "3":
                viewSentMsg(stubGetAll)
            elif opt == "4":
                listClients(stubClients)
            elif opt == "0":
                break

def on_response(ch, method, props, body):
    #global corr_id
    global response

    response = body

def send(toSend):
    global channel
    global callback_queue
    global corr_id
    global response
    arr = []

    response = None

    channel.basic_publish(
        exchange='',
        routing_key='server_queue',
        properties=pika.BasicProperties(
            #nombre de la cola a la que se le debe responder
            reply_to=callback_queue,
            #esta es solo una buena practica
            correlation_id=corr_id,
        ),
        #el mensaje se encuentra en body
        body=str(toSend))
    
    next = 1
    while next == 1:

        while response is None:
            connection.process_data_events()

        curr = str(response).split(";")
        response = None

        #print(str(response).split(";")[3])

        next = int(curr[5])
        arr.append(curr)

    channel.basic_consume(
        queue=callback_queue,
        on_message_callback=on_response,
        auto_ack=True)
    
    response = None
    
    return arr

response = None

conn = input("Please Introduce an IP: ")

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=conn))

channel = connection.channel()

#Primero se crea la cola con nombre aleatorio y el flag exclusive true
result = channel.queue_declare(queue='', exclusive=True)

callback_queue = result.method.queue

channel.basic_consume(
    queue=callback_queue,
    on_message_callback=on_response,
    auto_ack=True)

stubChat = "0"
stubClients = "1"
stubGetAll = "2"

###########################################
corr_id = str(uuid.uuid4())
###########################################

print("Would you like to run a simulation? y/n")
opt = input()
#opt = "y"

if opt == "y":
    print("y")
    simulation()
else:
    myMain(stubChat, stubClients, stubGetAll)