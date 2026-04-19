import random

import individuo

class AlgoritmoGenetico: 
    def __init__(self, tamanho_populacao, tamanho_cromossomo):
        self.tamanho_populacao = tamanho_populacao
        self.tamanho_cromossomo = tamanho_cromossomo
        self.populacao = []

    def inicializar_populacao(self):

        for _ in range(self.tamanho_populacao):
            cromossomo = []
            for _ in range(self.tamanho_cromossomo):
                cromossomo.append(random.randint(0, 6))
                cromossomo.append(random.randint(0, 1000))

            self.populacao.append(individuo.Individuo(cromossomo))

    def avaliar_populacao(self):
        pass

    def selecionar_pais(self):
        pass

    def crossover(self, pai1, pai2):
        pass

    def mutacao(self, cromossomo):
        pass

    def criar_nova_geracao(self):
        pass

    def executar(self):
        self.inicializar_populacao()
        
        for i, ind in enumerate(self.populacao):
            print(f"  > Testando indivíduo {i+1}/{self.tamanho_populacao}...")
            ind.calcular_fitness(redraw=True)
        

        pass