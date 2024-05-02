import time
import struct
import hashlib
import os
from FS_Transfer import FS_transfer
    ## TODO: falta ver que tamanho queremos
    # FS_Transfer_Protocol (que vai ser chamado após um pedido ao FS_Mediator)
    # É necessário multithreading

#Tamanhos dos componentes dos headers
ASK_SEND_FLAG = 2
HASH_SIZE = 32
FRAG_INDEX_SIZE = 32
FRAG_SIZE = 32
TIME_SIZE = 64
PAYLOAD=1024
#header de pedido para receber fragmento: Composto por 2bitflag, hash, fragIndex, fragSize + fill até 136 bits (38 bits fill)
HEADER_RECV = ASK_SEND_FLAG + HASH_SIZE + FRAG_INDEX_SIZE + FRAG_SIZE
#header de pedido para enviar fragmento: COmposto por 2bitflag, hash, fragIndex, timeSince + fill até 136 bits (6 bits fill)
HEADER_PING = ASK_SEND_FLAG + HASH_SIZE + FRAG_INDEX_SIZE + TIME_SIZE
HEADER_MAX = max(HEADER_PING,HEADER_RECV) + (8 - (max(HEADER_PING,HEADER_RECV) % 8)) #136 bits
PACKET_SIZE = HEADER_MAX + PAYLOAD
PAYLOAD_BYTES = (PAYLOAD + 7) // 8

class FS_Mediator:

    def __init__(self, sock, fragDir):
        self.sock = sock
        self.fragDir = fragDir
        self.transfer = FS_transfer(sock)

    def parseHeader (data): # recebe a data em bytes e retorna hashName em hex, payload em bytes e o resto em int
        
        bitString = ''.join(format(byte, '08b') for byte in data)

        #Flag do tipo de mensagem (Receber fragmento, enviar fragmento ou ping)
        tipoMsg = int(bitString[:ASK_SEND_FLAG])

        #Nome do hash de bin para hex
        hashName = format(int(bitString[ASK_SEND_FLAG:ASK_SEND_FLAG+HASH_SIZE], 2), f'0{HASH_SIZE//4}x')[2:]

        #Índice Fragmento
        fragIndex = int(bitString[ASK_SEND_FLAG+HASH_SIZE:ASK_SEND_FLAG+HASH_SIZE+FRAG_INDEX_SIZE])

        if(tipoMsg==2): ## Pedido de Ping (cálculo da diferença de tempo)
            endTime = int(time.time())
            startTimeBit = bitString[HEADER_PING-TIME_SIZE:HEADER_PING] # float tem tamanho de 64 bits 
            startTimeBytes = int(startTimeBit, 2).to_bytes(len(startTimeBit) // 8, byteorder='big')
            startTime = struct.unpack('>d', startTimeBytes)[0] #BUG Verificar isto

            return hashName, fragIndex, (endTime - startTime)

        if(tipoMsg==0): ## Receber Fragmentos

            # fragSize
            fragSize = int(bitString[HEADER_RECV-FRAG_SIZE:HEADER_RECV])

            # payload
            payload = bitString[HEADER_MAX:HEADER_MAX+fragSize].encode('utf-8')

            return hashName, fragIndex, fragSize, payload
        
        else: ## Pedido de envio de fragmentos
            
            return hashName, fragIndex
        
    def verifyHash(self,filePath,fileData,hashName,fragIndex):
        verHash = hashlib.shake_256(fileData).hexdigest(8)
        if(verHash == hashName):
            print(f"Fragment {hashName}_{fragIndex} has been received correctly")
            return 1
        else:
            os.remove(filePath)
            print(f"Verification of {hashName}_{fragIndex} failed. File removed and new request sent.")
            return 0
    

    def fastestConn(ipList):
        fastestIp = min(ipList, key=lambda x: x[1])
        return fastestIp

    def headerMediator(self,data,ip):
        if((data[0] & 0b11000000) == 0): ## Receber fragmentos

            hashName, fragIndex, fragSize, payload = self.parseHeader(data)

            filePath = self.fragDir + hashName + "_" + str(fragIndex)

            frag += payload[:fragSize]

            with open(filePath, 'w+b') as file:
                file.write(frag)
                fileData = file.read()

            if((self.verifyHash(filePath,fileData,hashName,fragIndex))==0): #Caso falhe a verificação
                self.transfer.askFrag(hashName,fragIndex,ip)
        
        elif(data[0] & 0b11000000 == 1): # Enviar fragmentos

            hashName, fragIndex = self.parseHeader(data)

            with open(self.fragDir + hashName + "_" + str(fragIndex), 'rb') as file:
                fragSize = len(file)
            
            #TODO: Falta ver onde vamos guardar a informação relevante a cada fragmento ou escrevemos em ficheiro até ficar completo
            self.transfer.sendFrag(self.sock,ip,fragSize,self.fragDir,hashName,fragIndex)

        else: # Ping

            hashName, fragIndex, tempo = self.parseHeader(data)
            #TODO: Adicionar uma tabela com chave hash+index+ip->tempo e chamar a função fastestConn

    def mediator(self, socket):
        while(True):
            data, addr = socket.recvfrom(1024)

            self.headerMediator(data,addr[0])
        