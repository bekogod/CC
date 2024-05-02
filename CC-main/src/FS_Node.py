import socket
import sys
import logging
import json
import hashlib
import ast
from FS_Tracker_Table import FS_Table
import threading
from FS_MSG import FS_Msg
from FS_Mediator import FS_Mediator

ONE_Bit = 1
ONE_B = 8
ONE_kbit = 1000
ONE_Kibit = 1024
ONE_kB = 8000
ONE_kiB = 8192
ONE_MB = 8000000
ONE_MiB = 8388608 

class FS_Node:

    def __init__(self, hostname, port ,trackerIp ):

        # self.startTime = datetime.now()
        self.soc = socket.socket(socket.AF_INET,     # Familia de enderecos ipv4
                                 socket.SOCK_STREAM)  # Connection-Oriented (TCP PROTOCOL)

        self.hostname = hostname
        self.endereco = socket.gethostbyname(self.hostname)
        self.porta = port
        self.soc.connect((trackerIp, self.porta))
        
        self.nodeId = f"{self.endereco}"
        self.contents = {} # Dict: { key=fileName: value=[fileSize, [Fragments], fileHash] }
        
        self.p2pInfo = {} # Dict: { key=}


    def sendTcpMsg(self, msg):

        message = msg.toText()

        try:
            self.soc.sendall(message.encode('utf-8'))
        except:
            print("Impossivel Conectar")
            return

        if msg.MSG_TYPE == "ASK FILE":

            message = self.soc.recv(1024)
            line = message.decode('utf-8')
            
            d = ast.literal_eval(line)
            
            for fileHash, lista in d.items():
                self.p2pInfo[fileHash] = lista
            
            # askFile : '8016d714d9cf5bb0', upLegion : '98d2da068043296c'
        
        else:
            pass


    def createMsg(self, MSG_TYPE, BODY={}):

        if MSG_TYPE == "UPDATE NODE":
            newBody = {}
            for value in self.contents.values():
                newBody[value[2]] = [value[0],value[1]]
            BODY = newBody

        msg = FS_Msg(self.hostname, self.endereco, MSG_TYPE, BODY)

        return msg
    
    def fragFile(self, filePath, fragSize):
        
        fragDir = "./frags/"
        
        fileName = filePath.split("/")[-1]
        
        with open(filePath, 'rb') as file:
            data = file.read()  
        
        frag = bytes([])    
        fragIndex = 0
        for byte in data:
            frag += bytes([byte])
            if len(frag) == fragSize:
                fragFile = open(fragDir + fileName + "_" + str(fragIndex), "wb" )
                fragFile.write(frag)
                frag = bytes([])
                fragIndex +=1
                 
        open(fragDir + fileName + "_" + str(fragIndex), "wb" )
        fragFile.write(frag)
        
        return fragIndex + 1
        
    def defragFile(self, fileName, numFrags):
        
        fileBytes = bytes([])    
        
        
        for fragIndex in range(numFrags):
            with open("." + fileName + "_" + str(fragIndex), 'rb') as fragBytes:
                data = fragBytes.read()
            fileBytes += data
        
        file = open(fileName, "wb" )
        file.write(fileBytes)

        

    def addFile(self, filePath):

        with open(filePath, 'rb') as file:
            data = file.read()  # .replace('\n',' ')
            hash256 = hashlib.shake_256(data).hexdigest(8)
            filename = filePath.split("/")[-1]
            name_hash = (hash256,filename)

        fileSize = len(data)
        if fileSize < ONE_Kibit:
            fragSize = ONE_B
        elif fileSize < ONE_kiB:
            fragSize = ONE_Kibit
        elif fileSize < ONE_MiB:
            fragSize = ONE_kiB
        else:
            fragSize = ONE_MiB

        self.fragFile(filePath,fragSize)
        
        numFrags = int(fileSize / fragSize)

        lastFragSize = fileSize - (numFrags * fragSize)

        if not lastFragSize == 0: numFrags += 1

        self.contents[name_hash[1]] = [fileSize, [True] * numFrags, name_hash[0]]

    def menu(self,node):
        while True:
            print("Node > ", end="")

            option = input()

            if option == "update":

                msg = node.createMsg("UPDATE NODE")
                node.sendTcpMsg(msg)

            elif option == "ask":
                file = input()

                BODY = {file: "NONE"}
                msg = node.createMsg("ASK FILE", BODY)
                node.sendTcpMsg(msg)

            elif option == "add":
                print("Insert File > ", end="")
                filePath = input()
                key = node.addFile(filePath)
                node.fragFile(filePath,node.contents[key][3])

            elif option == "list":

                print(json.dumps(node.contents, indent=4))

            elif option == "exit":

                msg = node.createMsg("DELETE NODE")
                node.sendTcpMsg(msg)
                node.soc.close()
                logging.info("Terminate normal execution")
                break

            else:
                logging.info("Unknown Option")


def main():

    host_name = sys.argv[1]
    port = int(sys.argv[2])
    tracker_ip = sys.argv[3]

    if len(sys.argv) > 1:
        node = FS_Node(host_name,port,tracker_ip)
    else:
        node = FS_Node()

    node.addFile("../msgs/askFile.msg")
    node.addFile("../msgs/updateLegionGusto.msg")
    
    # node.defragFile("askFile.msg",numfrags)
    
    msg = node.createMsg("UPDATE NODE")
    node.sendTcpMsg(msg)

    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO)
    
    while True:
        print("Node > ", end="")

        option = input()

        if option == "update":

            msg = node.createMsg("UPDATE NODE")
            node.sendTcpMsg(msg)

        elif option == "ask":
            body = {}
            while (True):
                print("Insert empty file hash to send!!\nInsert search file hash > ", end="")
                file = input()
                if file == "": break
                body[file] = "NONE"

            msg = node.createMsg("ASK FILE", body)
            
            # print("Insert File Name to store  > ", end="")
            # file = input()
            
            node.sendTcpMsg(msg)
            
            print (f"Onde estao: \n{json.dumps(node.p2pInfo)}")

        elif option == "add":
            print("Insert file name > ", end="")
            filePath = input()
            node.addFile(filePath)

        elif option == "list":

            print(json.dumps(node.contents, indent=4))

        elif option == "exit":

            msg = node.createMsg("DELETE NODE")
            node.sendTcpMsg(msg)
            node.soc.close()
            logging.info("Terminate normal execution")
            break
        elif option == "help":
        
            print("\nAvailable commands:")
            print("update - Update the node")
            print("ask    - Ask for a file with its hash")
            print("add    - Add a file to the node")
            print("list   - List the contents of the node")
            print("exit   - Exit the program\n")
        
        else:
            print("Unknown Option!!!\nTry help for options.")
    

if __name__ == "__main__":
    main()