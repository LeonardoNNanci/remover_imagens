import glob
import os
import platform
import shutil

import coleta_clima
import exifread

barra = ""

def inicializar():
    if platform.system() == 'Linux':
        busca = "/home/leo/Documentos/CC_UFF/IC/Imagens/"
        destino = "/home/leo/Documentos/CC_UFF/IC/cp/"
        barra = "/"
    elif platform.system() == 'Windows':
        busca = "G:\\Meu Drive\\Guanabara Bay - by month\\"
        destino = "G:\\Meu Drive\\Imagens Uteis\\"
        barra = "\\"

    verifica_pastas(busca, destino)
    coleta_clima.inicializar()
    
    return map(str, [busca, destino, barra])


def verifica_pastas(busca, destino):
    paths = glob.iglob(busca + "*" + barra)
    for path in paths:
        pasta = path[-8:]
        if not os.path.exists(destino + pasta):
            os.makedirs(destino + pasta)


def seleciona_imagens():
    busca, destino, barra = inicializar()
    count1 = count2 = count3 = count4 = 0
    
    arqs = glob.iglob(busca + "*" + barra + "*.jpg")
    for origem in arqs:
        #try:
        img = open(origem, "rb")
        data_hora = exifread.process_file(
            img, stop_tag='EXIF DateTimeOriginal')['EXIF DateTimeOriginal']
        data_hora = str(data_hora)
        img.close()

        hora = data_hora[11:13]
        hora = int(hora)

        if(6 <= hora < 18):
            # Reorganiza a string apara o formato YYYYMMDDHH
            data_hora = data_hora[:4] + data_hora[5:7] + \
                data_hora[8:10] + data_hora[11:13]

            visibilidade = coleta_clima.coleta(data_hora)['visibilidade']
            visibilidade = visibilidade.split()[-2]
            visibilidade = int(visibilidade)

            # Setar melhor horarios & visibilidade
            if(visibilidade > 5000):
                pasta = origem.split(barra)[-2] + barra
                shutil.copy2(origem, destino + pasta)
                count2 += 1
            else:
                count3 += 1
        else:
            count4 += 1
            
        count1+=1
        print("\rAnalisadas: %d | Selecionadas: %d | Visibilidade: %d | Horario: %d" %(count1, count2, count3, count4), end = "")
            
        #except Exception as e:
        #    print(e)
        #    exit()


if __name__ == '__main__':
    seleciona_imagens()
