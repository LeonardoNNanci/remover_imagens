import glob
import os
import shutil

import coleta_clima
import exifread


def mover_imagem(orig, dest):
    dest = dest + orig.split("/")[-2]
    if not os.path.exists(dest):
        os.makedirs(dest)
    shutil.copy2(orig, dest + "/")


destino = "/home/leo/Documentos/CC UFF/Iniciação Científica/cp/"
diretorios = glob.iglob(
    "/home/leo/Documentos/CC UFF/Iniciação Científica/Imagens/*/*.jpg")

for origem in diretorios:
    try:
        img = open(origem, "rb")
        data_hora = exifread.process_file(img, stop_tag='EXIF DateTimeOriginal')[
            'EXIF DateTimeOriginal']
        data_hora = str(data_hora)
        img.close()

        hora = data_hora[11:13]
        hora = int(hora)

        # Reorganiza a string apara o formato YYYYMMDDHH
        data_hora = data_hora[:4] + data_hora[5:7] + \
            data_hora[8:10] + data_hora[11:13]

        visibilidade = coleta_clima.coleta(data_hora)['visibilidade']
        visibilidade = visibilidade.split()[-2]
        visibilidade = int(visibilidade)

        # Setar melhor horários & visibilidade
        if((6 <= hora < 19) and (visibilidade > 5000)):
            mover_imagem(origem, destino)

    except Exception as e:
        print(e)
