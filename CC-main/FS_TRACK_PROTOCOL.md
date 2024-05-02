# FS TRACK PROTOCOL SYNTAX



Qualquer linha que comece por '#' é considerado um comentario e por isso ignorada na mensagem
Qualquer linha em branco deve ser ignorada

tipos de mensagens:

"UPDATE NODE"

"DELETE NODE"

"ASK FILE"


```markdown
(
# HEADER
SENDER_ID=Gusto;
SENDER_IP=127.0.1.10;
MSG_TYPE=UPDATE NODE;
# BODY
BODY={
FILE1 SIZE SEG=[...] ,
FILE2 SIZE SEG=[...] ,
FILE3 SIZE SEG=[...] 
};
)

```


No contexto deste nosso projeto ,implementamos um protocolo de comunicação por meio de uma conexão TCP, possibilitando a troca eficaz de dados entre os nodes e um servidor (tracker). Este protocolo por nos executado permite transmitir quatro tipos de mensagens, cada uma contendo quatro campos essenciais, com a flexibilidade de organizá-los em qualquer ordem. sendo estes campos.

SENDER_ID: Identifica o remetente da mensagem, fornecendo informações sobre o nodo de origem.
SENDER_IP: IP do nodo de origem
MSG_TYPE: Descreve a finalidade e a ação associada à mensagem, entre quatros opções mais abaixo especificadas.
BODY: Um campo opcional que pode conter informações adicionais relevantes para a mensagem. Ele também pode permanecer vazio, dependendo do tipo de mensagem específica.
Os quatro tipos de mensagem em nosso protocolo são os seguintes:

UPDATE NODE: Esta mensagem, iniciada por um nodo, transmite informações ao servidor. Ela abrange um SENDER_ID, SENDER_IP e tipo de Mensagem, enquanto que o corpo pode incluir uma lista de arquivos atualmente presentes no nodo. Alternativamente, o corpo pode estar vazio quando o nodo so quer informar o tracker que existe.

DELETE NODE: Esta mensagem sinaliza a remoção de um nodo da rede. Ela inclui o SENDER_ID, SENDER_IP e tipo de Mensagem, mas não apresenta um corpo de mensagem.

ASK FILE: Esta mensagem serve para um nodo pedir ao servidor sobre os ficheiros enumerados na propria mensagem. Ela inclui o SERVER_IP SERVER_ID e o tipo de mensagem como campos, descartando um "body"

END TRACKER: Serve como um sinal para o término da do tracker, esta mensagem inclui o  SENDER_ID, SENDER_IP e tipo de Mensagem.
