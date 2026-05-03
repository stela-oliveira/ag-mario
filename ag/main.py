import os
import sys

# Adiciona o diretório raiz ao path para encontrar o pacote 'data'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import algoritmo_genetico_otimizado

# Configurações do Algoritmo Otimizado
# tamanho_janela: quantos movimentos evoluem ao mesmo tempo
# genes_para_fixar: quantos movimentos são "consolidados" no prefixo por vez
ag = algoritmo_genetico_otimizado.AlgoritmoGeneticoOtimizado(
    tamanho_populacao=20, 
    tamanho_janela=10, 
    genes_para_fixar=2
)

# Loop de evolução contínua
try:
    while True:
        ag.evoluir(n_geracoes=1)
except KeyboardInterrupt:
    print("\nInterrompido pelo usuário. Salvando melhor resultado...")
    ag.salvar_melhor("melhor_resultado_final_paralelismo")