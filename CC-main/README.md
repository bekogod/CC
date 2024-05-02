<img src='uminho.png' width="30%"/>

<h3 align="center">Licenciatura em Engenharia Informática <br> Trabalho prático de Comunicação de Dados <br> 2023/2024 </h3>

---


## Transferência rápida e fiável de múltiplos servidores em simultâneo

A partilha de ficheiros em redes é crucial para transferências fiáveis e livres de erros. Este trabalho busca desenvolver um serviço avançado de transferência de ficheiros em uma rede peer-to-peer (P2P) com múltiplos servidores que também atuam como clientes. A ideia é que os pares na rede se comuniquem entre si, permitindo a transferência simultânea de partes de um ficheiro de vários peers para melhorar a disponibilidade e o desempenho. Inspirado em redes como o "BitTorrent". 

---
<h3 align="center"> Equipa</h3>

<div align="center">

| Nome           | Número |
| -------------- | ------ |
| Augusto Campos | A93320 |
| Carlos Silva   | A93199 |
| Bernardo Lima  | A93258 |

</div>

## Requesitos

### Requesitos Gerais

- [ ] O FS_Node deve registar-se e manter-se conectado a um FS_Tracker
- [ ] O FS_Node deve manter o FS_Tracker atualizado em relação à lista de blocos a seu cargo
- [ ] O sistema deve permitir a entrada e saída de novos servidores FS_Node a qualquer momento

### Fase 1 - FS Track Protocol (TCP)

Requisitos:

 O protocolo FS TRACK Protocol deve funcionar sobre TCP e suportar:

- [X] O registo de um FS_NODE
- [X] A Atualizacao de lista de ficheiros e blocos disponiveis num FS_NODE
- [X] O pedido de localizacao de um ficheiro devolvendo uma lista de FS_NODE e blocos neles disponiveis

Especificar o protocolo FS Track Protocol para funcionar sobre TCP

- [ ] formato das mensagens protocolares (sintaxe)  
- [ ] função e significado dos campos (semântica)
- [X] diagrama temporal ilustrativo (comportamento)

### FASE 2 - FS Transfer Protocol (UDP)

O protocolo FS Transfer Protocol deve funcionar sobre UDP e suportar:
  
- [ ] Aceitar pedidos de blocos, em paralelo, de múltiplos outros FS_Node
- [ ] Pedir, em paralelo, blocos do mesmo ficheiro a múltiplos FS_Node
- [ ] Suportar cenários de perda de blocos, garantindo uma entrega fiável

Etapas sugeridas para esta fase:

- [ ] Especificar o protocolo FS Transfer Protocol para funcionar sobre UDP   
  - [ ] Formato dos datagramas
  - [ ] o Modo de funcionamento
- [ ] Implementação e teste no cenário proposto