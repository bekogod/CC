import json
class FS_Msg:
    def __init__(self,
        SENDER_ID = "NO VALUE",  
        SENDER_IP = "NO VALUE",  
        MSG_TYPE = "NO VALUE",
        BODY = {} # Only used for MSG_TYPE=UPDATE NODE
        ):
        
        self.SENDER_ID  = SENDER_ID
        self.SENDER_IP  = SENDER_IP  
        self.MSG_TYPE   = MSG_TYPE
        self.BODY       = BODY
        

    def __str__(self):

        out = ""
        out += "Message = { \n"
        out += f"SENDER_ID = {self.SENDER_ID}\n"
        out += f"SENDER_IP = {self.SENDER_IP}\n"
        out += f"MSG_TYPE = {self.MSG_TYPE}\n"
        out += f"BODY = {json.dumps(self.BODY, indent=4)}\n"
        out += "}"

        return out

    def __repr__(self):

        out = ""
        out += "Message = { \n"
        out += f"SENDER_ID = {self.SENDER_ID}\n"
        out += f"SENDER_IP = {self.SENDER_IP}\n"
        out += f"MSG_TYPE = {self.MSG_TYPE}\n"
        out += f"BODY = {self.BODY}\n"
        out += "}"

        return out
    
    def toText(self):
        out = "("
        out += F"SENDER_ID={self.SENDER_ID};\n"
        out += F"SENDER_IP={self.SENDER_IP};\n"
        out += F"MSG_TYPE={self.MSG_TYPE};\n"
        out += "BODY={\n"
        if self.MSG_TYPE == "UPDATE NODE":
            for file in self.BODY:
                fragments = "["
                for frag in self.BODY[file][1]:
                    if frag: fragments += "1"
                    else: fragments += "0"
                fragments += "]"
                out += f"{file} {self.BODY[file][0]} {fragments},\n"
            out += "};"
        elif self.MSG_TYPE == "ASK FILE":
            askingList = ""
            for file in self.BODY:
                askingList += f"{file},\n"
            out += askingList
            out += "};" 
        else:
            out += "};"
        out += ")"
        return out

    def read_message(self, data):
        # pckg = ""
        
        # for line in data.split('\n'):
        #     if not (line == '' or line[0] == '#' ):
        #         pckg += line
        
        
        if data[0] == '(' and data[-1] == ')':
            data = data[1:-1]
        else:
            return False
            
            
                

        for field in data.split(";"):
            element = field.split("=")

            if element[0] == "SENDER_ID":
                self.SENDER_ID = element[1]
            if element[0] == "SENDER_IP":
                self.SENDER_IP = element[1]
            elif element[0] == "MSG_TYPE":
                self.MSG_TYPE = element[1]
            elif element[0] == "BODY":
                self.BODY = {}
                bodyLines = element[1].strip("\{\} ").split(",")
                
                if self.MSG_TYPE == "UPDATE NODE":
                                            
                    for line in bodyLines:
                        if line != "":
                            elems = line.split(" ")
                            
                            nodeId = elems[0]
                            fileSize = int(elems[1])
                            fragments = []
                            for char in elems[2]:
                                if char == "0": fragments.append(False)
                                elif char == "1": fragments.append(True)
                                else: pass 
                                
                            self.BODY[nodeId] = [fileSize,fragments]
                            
                elif self.MSG_TYPE == "ASK FILE":
                    for line in bodyLines:
                        if line != "":
                            self.BODY[line] = "NONE"
                else:
                    pass      
            else:
                pass
        
        return True
