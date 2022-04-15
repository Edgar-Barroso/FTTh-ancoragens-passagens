#pip install geopy.distance
#pip install os
#pip install shutil
#pip install zipfile
#pip install xmltodict
#pip install xml.etree.ElementTree

import shutil
import os
from geopy.distance import distance


# Hiperparametros

# distancia aceitavel em Metros para considerar que o cabo passa naquele poste
distancia_min_cabo_poste = 4

# angulação em Graus para o programa determinar tal ponto como
angulo_ancoragem = 15

#arquivos
dic_cabos = 'Cabos.kmz'
dic_ceos = 'CEOs.kmz'
dic_postes = 'Postes.kmz'




from ponto import Ponto
from caminho import Caminho

cabos = Caminho.extrair_caminhos(dic_cabos)
caixas = Ponto.extrair_pontos(dic_ceos)
postes = Ponto.extrair_pontos(dic_postes)  # OPCIONAL

for cabo in cabos:
    for n, coord in enumerate(cabo.coordenadas):
        menor = distancia_min_cabo_poste
        escolhido = coord
        for poste in postes:
            dist = distance(poste.coordenada, coord)
            if dist < menor:
                menor = dist
                escolhido = poste.coordenada
        cabo.coordenadas[n] = escolhido

for cabo in cabos:
    ancs = cabo.ancoragens(angulo_ancoragem)
    for anc in ancs:
        for caixa in caixas:
            if (caixa - anc) < 3:
                anc.nome = 'ancoragem'
                break
    for n, p in enumerate(ancs):
        if p.nome == 'passagem' and ancs[n - 1].nome == 'passagem':
            p.nome = 'ancoragem'
    ac = -1
    ps = 0
    for c in ancs:
        if c.nome == 'ancoragem':
            ac += 1
        elif c.nome == 'passagem':
            ps += 1
    encontrados = []
    for c in cabo.coordenadas:
        if c not in encontrados:
            encontrados.append(c)
    cabo.coordenadas = encontrados


    print(f'{cabo.nome} \n{ac} postes com ancoragem\n{ps} postes com passagem\n')



try:
    shutil.rmtree(f'{os.getcwd()}\TEMP')
except FileNotFoundError:
    pass
