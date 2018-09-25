import os

from metar import Metar


def coleta(data_hora):
    try:
        os.system(
            "wget --user-agent=\"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)\" --base=\"http://www.redemet.aer.mil.br/api/consulta_automatica/index.php\" --referer=\"http://www.redemet.aer.mil.br/api/consulta_automatica/index.php\" --post-data=\"&local=sbrj&msg=metar&data_ini=" + data_hora + "&data_fim=" + data_hora + "\" -O resultado.txt http://www.redemet.aer.mil.br/api/consulta_automatica/index.php")
        d = {}
        linha = open("resultado.txt", 'r').readline()
        traduzido = Metar.Metar(linha[13:-2])

        vento = traduzido.wind()
        vento_dir = str(traduzido.wind_dir)
        vento_vel = vento.split(" ")[2]

        nuvens = traduzido.sky_conditions()
        visibilidade = traduzido.visibility()
        temperatura = str(traduzido.temp)
        pressao = str(traduzido.press)

        d['vento'] = [vento_dir, vento_vel]
        d['nuvens'] = nuvens
        d['visibilidade'] = visibilidade
        d['temperatura'] = temperatura
        d['pressao'] = pressao

        return d

    except IOError:
        return 0
