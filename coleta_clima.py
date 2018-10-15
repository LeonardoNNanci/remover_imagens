import os
import platform

from metar import Metar


def comando_linux(data_hora):
    comando = "wget --user-agent=\"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)\" --base=\"http://www.redemet.aer.mil.br/api/consulta_automatica/index.php\" --referer=\"http://www.redemet.aer.mil.br/api/consulta_automatica/index.php\" --post-data=\"&local=sbrj&msg=metar&data_ini=" + \
        data_hora + "&data_fim=" + data_hora + \
        "\" -O resultado.txt http://www.redemet.aer.mil.br/api/consulta_automatica/index.php"
    os.system(comando)


def comando_windows(data_hora):
    comando = "wget/wget.exe --user-agent=\"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)\" --base=\"http://www.redemet.aer.mil.br/api/consulta_automatica/index.php\" --referer=\"http://www.redemet.aer.mil.br/api/consulta_automatica/index.php\" --post-data=\"&local=sbbr,sbgl,sbpa&msg=metar,taf&data_ini=" + data_hora + "&data_fim=" + data_hora + " -O resultado.txt http://www.redemet.aer.mil.br/api/consulta_automatica/index.php"
    os.system(comando)

def comando_windows(data_hora):
    pass


def inicializar():
    global comando
    if platform.system() == 'Linux':
        comando = comando_linux
    elif platform.system() == "Windows":
        comando = comando_windows


def coleta(data_hora):
    try:
        comando(data_hora)
        d = {}
        linha = open("resultado.txt", 'r').readline()
        traduzido = Metar.Metar(linha[13:-2])

        # vento = traduzido.wind()
        # vento_dir = str(traduzido.wind_dir)
        # vento_vel = vento.split(" ")[2]

        nuvens = traduzido.sky_conditions()
        visibilidade = traduzido.visibility()
        temperatura = str(traduzido.temp)
        pressao = str(traduzido.press)

        # d['vento'] = [vento_dir, vento_vel]
        d['nuvens'] = nuvens
        d['visibilidade'] = visibilidade
        d['temperatura'] = temperatura
        d['pressao'] = pressao

        return d

    except IOError as e:
        print(e)
        return 0
