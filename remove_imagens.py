import glob
import os

import coleta_clima
import exifread

imgs = glob.iglob(
    "/home/leo/Documentos/CC UFF/Iniciação Científica/Imagens/*/*.jpg")
for i in imgs:

    try:
        img = open(i, "rb")
        data_hora = exifread.process_file(img, stop_tag='EXIF DateTimeOriginal')[
            'EXIF DateTimeOriginal']
        data_hora = str(data_hora)
        img.close()

        hora = data_hora[11:13]
        hora = int(hora)

        if(hora < 6 or hora > 19):   # Setar melhor horários
            os.remove(i)

        else:
            # Reorganiza a string apara o formato YYYYMMDDHH
            data_hora = data_hora[:4] + data_hora[5:7] + \
                data_hora[8:10] + data_hora[11:13]

            visibilidade = coleta_clima.coleta(data_hora)['visibilidade']
            visibilidade = visibilidade.split()[-2]
            visibilidade = int(visibilidade)

            if(visibilidade < 5000):  # Setar melhor visibilidade
                os.remove(i)

    except:
        exit()
