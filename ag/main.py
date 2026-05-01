import os
import sys

# Adiciona o diretório raiz ao path para encontrar o pacote 'data'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import algoritmo_genetico

ag = algoritmo_genetico.AlgoritmoGenetico(5, 5)

ag.executar()