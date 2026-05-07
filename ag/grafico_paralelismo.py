import json
import matplotlib.pyplot as plt

with open('../historico_paralelismo.json') as f:
    historico = json.load(f)

geracoes = [h['geracao'] for h in historico]
fitness  = [h['fitness']  for h in historico]

plt.plot(geracoes, fitness)
plt.xlabel('geração')
plt.ylabel('fitness')
plt.title('Evolução do Fitness — COM Paralelismo')
plt.tight_layout()
plt.savefig('evolucao_paralelismo.png', dpi=150)
plt.show()
print('Gráfico salvo em evolucao_paralelismo.png')