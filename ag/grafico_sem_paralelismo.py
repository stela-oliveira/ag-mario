import json
import matplotlib.pyplot as plt

with open('../historico_sem_paralelismo.json') as f:
    historico = json.load(f)

geracoes = [h['geracao'] for h in historico]
fitness  = [h['fitness']  for h in historico]

plt.plot(geracoes, fitness, color='orange')
plt.xlabel('geração')
plt.ylabel('fitness')
plt.title('Evolução do Fitness — SEM Paralelismo')
plt.tight_layout()
plt.savefig('evolucao_sem_paralelismo.png', dpi=150)
plt.show()
print('Gráfico salvo em evolucao_sem_paralelismo.png')