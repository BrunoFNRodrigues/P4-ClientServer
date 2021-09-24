#####################################################
# Camada Física da Computação
#Carareto
#11/08/2020
#Aplicação
####################################################


#esta é a camada superior, de aplicação do seu software de comunicação serial UART.
#para acompanhar a execução e identificar erros, construa prints ao longo do código! 


from enlace import *
import time
import numpy as np
import random
import binascii
from utils import *


# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

#use uma das 3 opcoes para atribuir à variável a porta usada
#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
# serialName = "COM3"                  # Windows(variacao de)


def main():
    try:
        #declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
        #para declarar esse objeto é o nome da porta.
        com3 = enlace('COM3')
        com3.enable()
        print("ON")

        imageR = "D:/Faculdade/4_semestre/FisComp/P4-ClientServer/imgs/image.png"

        txBuffer = open(imageR, "rb").read()
        packs = Pack(txBuffer)
        numPck = len(packs)
        lenPayload =  (numPck).to_bytes(1, byteorder='big')

        #Estados
        inicia = False
        validado = False

        #Handshake
        while inicia == False:
            if validado == False:
                pergunta=input("Você quer continuar (s/n):")
                if pergunta == "s":
                    com3.sendData(np.asarray(Datagrama(tipo="1", npacks=numPck)))
                    msgt1, nrx = com3.getData(14, 5)
                    validado = msgt1[0:1] == b'\x02'
                    print("Validação:", validado)
                elif pergunta == 'n':
                    com3.disable()
                    exit()          
            else:
                inicia = True
        #Enviando dados
        cont = 1
        
        while cont <= numPck:
            print("Enviando Pacote", cont)
            pacote = Datagrama(tipo="3", npacks=numPck, num_pack=cont, payload_len=len(packs[cont-1]), payload=packs[cont-1])
            com3.sendData(np.asarray(pacote))
            print("Pacote {}/{}".format(cont,numPck), pacote)
            start_timer1 = time.time()
            start_timer2 = time.time()
            msgt4, nRx = com3.getData(14)

            if msgt4[0:1] == b'\x04':
                cont += 1
            else:
                deu_ruim = True
                while deu_ruim == True:
                    print("deu ruim")
                    if time.time()-start_timer1 > 5:
                        pacote = Datagrama(tipo="3", npacks=numPck, num_pack=cont, payload_len=len(packs[cont-1]), payload=packs[cont-1])
                        com3.sendData(np.asarray(pacote))
                        start_timer1 = time.time()
                    if time.time()-start_timer2 > 20:
                        com3.sendData(np.asarray(Datagrama(tipo="5")))
                        com3.disable()
                        print("(╯ ͠° ͟ʖ ͡°)╯┻━┻")
                        exit()
                    else:
                        msgt6, nRx = com3.getData(14)
                        if msgt6[0:1] == b'\x06':
                            cont = int.from_bytes(msgt6[7:8], "big")
                            pacote = Datagrama(tipo="3", npacks=numPck, num_pack=cont, payload_len=len(packs[cont-1]), payload=packs[cont-1])
                            start_timer1 = time.time()
                            start_timer2 = time.time()
                            
                        msgt4, nRx = com3.getData(14)
                        if msgt4[0:1] == b'\x04':
                            cont += 1
                            deu_ruim = False





        

        
         
    
        # Encerra comunicação
        print("-------------------------")
        print("Comunicação encerrada")
        print("-------------------------")
        com3.disable()       
        
    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com3.disable()      

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
