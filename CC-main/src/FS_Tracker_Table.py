import json


class FS_Table:
    def __init__(self):
        self.contents = {}  # Inicia o nodo vazio
        # self.node_addresses = {} # Inicializa o endereço do nodo

    def __str__(self):

        out = ""
        out += json.dumps(self.contents, indent=4)
        # out += f"{self.node_addresses} \n"

        return out

    def __repr__(self):

        out = ""
        out += json.dumps(self.contents, indent=4)
        # out += f"{self.node_addresses} \n"

        return out

    def addNode(self, node_id):
        # Adiciona um nodo ao tracker
        # self.node_id = node_id
        if node_id not in self.contents:
            self.contents[node_id] = {}
        return node_id

    def updateNode(self, node_id, body):
        # Adiciona um node e a info dos ficheiros nele contidos        
        self.addNode(node_id)
        
        for newFile in body:    
            self.contents[node_id][newFile] = body[newFile] 
        
    # def updateFragments(self, node_id, file_id, fragments):  # incluir lista de fragmentos
    #     # Dá update ao fragmento de um ficheiro para um dado estado (Tanto para adicionar como remover)
    #     if self.contents[node_id][file_id]:
    #         i = 0
    #         while i < 20:
    #             self.contents[node_id][file_id][1][i] = fragments[i]
    #             i += 1

    # def addCompleteNode(self, nodeId, address, fragments, fileId):
    #     self.addNode(nodeId, address)
    #     self.addFileFragments(nodeId, fileId)
    #     self.updateFragments(nodeId, fileId, fragments)

    # def removeFileFromNode(self, node_id, file_id):
    #     # Remove um ficheiro de um nodo
    #     if node_id in self.contents and file_id in self.contents[node_id]:
    #         del self.contents[node_id][file_id]

    def removeNode(self, node_id):
        # Remove a node and all its associated information from the table
        if node_id in self.contents:
            del self.contents[node_id]
        # if node_id in self.node_addresses:
        #     del self.node_addresses[node_id]

    # def getFragmentStatus(self, node_id, file_id):
    #     # Verifica o estado de fragmentos de um ficheiro (Para verificação manual?)
    #     if node_id in self.contents and file_id in self.contents[node_id]:
    #         return self.contents[node_id][file_id]
    #     else:
    #         return None

    # def getNodesWithFragment(self, file_id, fragment_index):
    #     # Retorna os nodos que têm um fragmento de um ficheiro
    #     nodes_with_fragment = []
    #     for node_id, files in self.contents.items():
    #         if file_id in files:
    #             fragments = files[file_id]
    #             if 0 <= fragment_index < 20 and fragments[fragment_index]:
    #                 nodes_with_fragment.append(node_id)
    #     return nodes_with_fragment

    def getNodesWithFilename(self, body):
        # Verifica os nodos que têm os ficheiros referenciados na msg
        nodes_with_filename = {}
        for search_file in body:
            nodes_with_filename[search_file] = []
            for node_id, files in self.contents.items():
                if search_file in files:
                    nodes_with_filename[search_file].append( (node_id,files[search_file]))
        
        return nodes_with_filename

    # def getContents(self):
    #     # Retorna a tabela de nodos
    #     return self.contents

    # def getNodeAddress(self, node_id):
        # Retorna o endereço de um nodo
        # return self.node_addresses.get(node_id)

    def writeTable(self):
        string = []

        for node_id in self.contents.items():
            string.append("\nNodo->")
            string.append(node_id)
            string.append("Ficheiros->")
            for files in self.contents[node_id]:
                string.append(files)
                string.append(", ")

        return string
