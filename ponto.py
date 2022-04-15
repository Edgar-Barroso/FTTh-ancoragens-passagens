import xml.etree.ElementTree as el
from geopy.distance import distance

import zipfile
class Ponto:
    def __init__(self, coordenada=None):
        self._coordenada = coordenada

    @property
    def coordenada(self):
        return self._coordenada

    @coordenada.setter
    def coordenada(self, valor):
        if type(valor) is not list:
            raise ValueError('coordenada deve ser uma list')
        self._coordenada = valor

    @classmethod
    def extrair_pontos(cls, arq_name):
        lista = []
        if '.kmz' in arq_name:
            with zipfile.ZipFile(arq_name, 'r') as f:
                f.extract('doc.kml', 'TEMP')
                arq_name = 'TEMP\doc.kml'
        doc = el.parse(arq_name)
        root = doc.getroot()
        np = root.tag.split('}')[0] + '}'
        for c in root.iter(np + 'Placemark'):
            ponto = False
            pt = Ponto()
            for j in c:
                if j.tag == f'{np}name':
                    pt.nome = j.text
                elif j.tag == f'{np}Point':
                    ponto = True
                    for q in j:
                        if q.tag == f'{np}coordinates':
                            pt.coordenada = [float(q.text.strip().split(',')[1]),float(q.text.strip().split(',')[0])]

            if ponto is True:
                lista.append(pt)
        return lista

    def __sub__(self, other):
        return distance(self.coordenada, other.coordenada).meters
