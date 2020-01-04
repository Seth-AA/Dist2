from datetime import datetime
import logging
from random import choices, choice

import grpc

import act1.Act1_pb2 as Act1_pb2
import act1.Act1_pb2_grpc as Act1_pb2_grpc

ClientName = ""

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
    req = Act1_pb2.Act1Request(Username = ClientName)
    response = stub.HandShake(req)
    print(response.Msg)
    return response

def listClients(stub):
    global ClientName

    req = Act1_pb2.basicMsg(From = ClientName,
                            Msg = "getClients")
    response = stub.GetClients(req)

    i = 1
    print("The following is the list of current Clients in the Server: ")
    for usr in response:
        print("%i - %s" % (i, usr.Username))
        i += 1

def sendMsg(stub, dest = "", msg = ""):
    print("Indicate the username to which you want to send a message")
    if dest == "":
        dest = input("Username: ")
        msg = input("Message: ")
    else:
        print("Username: %s" % dest)
        print("Message: %s" % msg)
    time = datetime.now().strftime("%b-%d-%Y %H:%M:%S")

    req = Act1_pb2.FullMsg(From = ClientName,
                            To = dest, 
                            Msg = msg, 
                            Date = time)
    response = stub.Dispatch(req)
    print(response.Msg)

def viewSentMsg(stub):

    req = Act1_pb2.basicMsg(From = ClientName,
                            Msg = "getSentMsgs")
    response = stub.GetAllSent(req)

    for msg in response:
        if msg.From == "server":
            print(msg.Msg)
            break
        print("[%s] To: %s" % (msg.Date, msg.To))
        print("Message: %s" % msg.Msg)

def viewReceivedMsg(stub):
    req = Act1_pb2.basicMsg(From = ClientName,
                            Msg = "getReceivedMsgs")
    response = stub.Retrieve(req)

    for msg in response:
        if msg.From == "server":
            print(msg.Msg)
            break
        print("[%s] From: %s" % (msg.Date, msg.From))
        print("Message: %s" % msg.Msg)

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

def simulation(stubChat, stubClients, stubGetAll):
    
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


def run():
    channel = grpc.insecure_channel('s1:50051')
    #Make all the stubs
    stubChat = Act1_pb2_grpc.ChatStub(channel)
    stubClients = Act1_pb2_grpc.ClientsStub(channel)
    stubGetAll = Act1_pb2_grpc.GetAllStub(channel)

    print("Would you like to run a simulation? y/n")
    #opt = input()
    opt = "y"
    print(opt)
    if opt == "y":
        simulation(stubChat, stubClients, stubGetAll)
    else:
        myMain(stubChat, stubClients, stubGetAll)

    # response = logIn(stubChat)
    # print(response)
    # listClients(stubClients)

if __name__ == '__main__':
    logging.basicConfig()
    run()