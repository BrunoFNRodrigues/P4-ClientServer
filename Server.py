from enlace import *
import time
import numpy as np
from utils import *

def main():
    try:
        #declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
        #para declarar esse objeto é o nome da porta.
        com4 = enlace('COM4')
        # Ativa comunicacao. Inicia os threads e a comunicação seiral 
        com4.enable()
        #Se chegamos até aqui, a comunicação foi aberta com sucesso. Faça um print para informar.
        print("ON")
        #aqui você deverá gerar os dados a serem transmitidos. 
        imageW = "D:/Faculdade/4_semestre/FisComp/P4-ClientServer/imgs/recebidaCopia.png"
        SaveImage = open(imageW, 'wb')
        ocioso = True 

        while ocioso == True:
            print("Ocioso")
            msgt1, nrx = com4.getData(14)
            if msgt1[0:1] == b'\x01':
                if msgt1[2:3] == b'\x0F':
                    ocioso = False
            time.sleep(1)
        print("Estou vivo!!!")

        com4.sendData(np.asarray(Datagrama(tipo="2")))
        cont = 1
        numPck = int.from_bytes(msgt1[3:4], "big")

        while cont <= numPck:
            print("Recebendo Pacote",cont)
            start_timer1 = time.time()
            start_timer2 = time.time()

            msgt3, nrx = com4.getData(10)
            payload_len = int.from_bytes(msgt3[5:6], "big")
            payload, nrx = com4.getData(payload_len)
            eop, nrx = com4.getData(4)
            print("Pacote {}/{}".format(cont,numPck), payload)
            n_pack = int.from_bytes(msgt3[4:5], "big")
            if msgt3[0:1] == b'\x03':
                if n_pack == cont and eop == b'\xFF\xAA\xFF\xAA':
                    cont += 1
                    com4.sendData(np.asarray(Datagrama(tipo="4")))
                    SaveImage.write(payload)
                else:
                    com4.sendData(np.asarray(Datagrama(tipo="6")))
            else:
                time.sleep(1)
                if time.time()-start_timer2 > 20:
                    ociosso = True
                    com4.sendData(np.asarray(Datagrama(tipo="5")))
                    print("( ͡ಥ ͜ʖ ͡ಥ)")
                    com4.disable()
                    exit()
                else:
                    if time.time()-start_timer1 > 2:
                        com4.sendData(np.asarray(Datagrama(tipo="4")))
                        start_timer1 = time.time()

        SaveImage.close()
    
        # Encerra comunicação
        print("-------------------------")
        print("Comunicação encerrada")
        print("-------------------------")
        com4.disable()        
        
    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com4.disable()        

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
