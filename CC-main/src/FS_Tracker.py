import socket
import threading
import logging
import sys
from FS_Tracker_Table import FS_Table
from FS_MSG import FS_Msg

class FS_Tracker:


    def __init__(self,hostName, port = 9090):

        # self.startTime = datetime.now()
        self.table = FS_Table()
        self.hostname = hostName
        self.endereco = socket.gethostbyname(self.hostname)  
        self.porta = port
        
    
    def openTcpConnection(self):
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
        soc.bind((self.endereco, self.porta))            
        soc.listen()
        

        while True:
            connection, address = soc.accept() 
            tcp = threading.Thread(target=self.launchTcpConnection,args=(connection, address))
            tcp.start()
        
    def launchTcpConnection(self,connection, address):
        
        msg = ""
        
        while True:
            data = connection.recv(1024)
            fullMessage = True
            
            if data:
                data_received = data.decode('utf-8')
                
                # Cleaning empty lines and comments
                pckg = ""
        
                for line in data_received.split('\n'):
                    if not (line == '' or line[0] == '#' ):
                        pckg += line
                
                
                # Checking message delimiters
                index = 0
                indexStart = 0
                indexEnd = 0
                for char in pckg:
                    if char == '(': indexStart = index
                    if char == ')': 
                        indexEnd   = index
                        break
                    index += 1
                
                if indexEnd == 0:
                    fullMessage = False
                
                current_message = pckg[indexStart:indexEnd+1]
                msg = pckg[indexEnd+1:]
                
                # print("Received message: " + current_message)
                # print("Leftover data: " + msg)
                
                message = FS_Msg()
                message.read_message(current_message)
                
                if fullMessage:
                    logging.info("Received TCP message")
                    
                    if message.MSG_TYPE == "UPDATE NODE":
                        self.table.updateNode(message.SENDER_ID,message.BODY)
                        logging.info(f"UPDATE: {message.SENDER_ID}@{message.SENDER_IP}")

                    elif message.MSG_TYPE == "DELETE NODE":
                        
                        self.table.removeNode(message.SENDER_ID)
                        logging.info(f"REMOVE: {message.SENDER_ID}@{message.SENDER_IP}")
                        
                    elif message.MSG_TYPE == "ASK FILE":
                        
                        node_list = self.table.getNodesWithFilename(message.BODY)
                        connection.send(str(node_list).encode('utf-8'))
                        logging.info(f"ASK RESPONSE: {message.SENDER_ID}")
                        
                    elif message.MSG_TYPE == "END TRACKER":
                        pass
                    else:
                        logging.error(f"INVALID MESSAGE FROM NODE: {message.MSG_TYPE}")
                    # clean msg
                    msg = ""
                else:
                    pass
                    
            else:
                logging.info(f"Closing connection {address}")
                break
            
        
        
            
def main():
    
    tracker_name = sys.argv[1]
    port = int(sys.argv[2])
    
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO)
    
    tracker = FS_Tracker(tracker_name,port)
    
    tracker.openTcpConnection()    
    
        
    logging.info("ENDED NORMAL EXECUTION")

    
if __name__ == "__main__":
    main()