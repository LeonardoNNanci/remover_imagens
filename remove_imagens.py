import glob
import os
import shutil

import coleta_clima
import exifread


def __init__():
    if os.uname().sysname == 'Linux':
        busca = "/home/leo/Documentos/CC_UFF/IC/Imagens/"
        destino = "/home/leo/Documentos/CC_UFF/IC/cp/"
    elif os.uname().sysname == 'Win32':
        busca = ""
        detino = ""

    verifica_pastas(busca, destino)
    coleta_clima.__init__()

    return map(str, [busca, destino])


def verifica_pastas(busca, destino):
    paths = glob.iglob(busca + "*/")
    for path in paths:
        pasta = path[-8:]
        if not os.path.exists(destino + pasta):
            os.makedirs(destino + pasta)


def seleciona_imagens():
    busca, destino = __init__()

    arqs = glob.iglob(busca + "*/*.jpg")

    for origem in arqs:
        try:
            img = open(origem, "rb")
            data_hora = exifread.process_file(
                img, stop_tag='EXIF DateTimeOriginal')
            data_hora = data_hora['EXIF DateTimeOriginal']
            data_hora = str(data_hora)
            img.close()

            hora = data_hora[11:13]
            hora = int(hora)

            # Reorganiza a string apara o formato YYYYMMDDHH
            data_hora = data_hora[:4] + data_hora[5:7] + \
                data_hora[8:10] + data_hora[11:13]

            visibilidade = coleta_clima.coleta(data_hora)
            visibilidade = visibilidade['visibilidade']
            visibilidade = visibilidade.split()[-2]
            visibilidade = int(visibilidade)

            # Setar melhor horarios & visibilidade
            if((6 <= hora < 19) and (visibilidade > 5000)):
                pasta = origem.split("/")[-2] + "/"
                shutil.copy2(origem, destino + pasta)

        except Exception as e:
            print(e)
            exit()


if __name__ == '__main__':
    seleciona_imagens()
