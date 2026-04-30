import random

import individuo
import serializer as s
import populacao as p

class AlgoritmoGenetico: 
    def __init__(self, tamanho_populacao, tamanho_cromossomo):
        self.tamanho_populacao = tamanho_populacao
        self.tamanho_cromossomo = tamanho_cromossomo
        self.populacao = p.Populacao()

    def inicializar_populacao(self):

        for _ in range(self.tamanho_populacao):
            cromossomo = []
            for _ in range(self.tamanho_cromossomo):
                cromossomo.append(random.randint(0, 6))
                cromossomo.append(random.randint(0, 1000))

            self.populacao.add_individuo(individuo.Individuo(cromossomo))

    def avaliar_populacao(self, populacao: p.Populacao):
        for ind in populacao.individuos:
            ind.calcular_fitness(redraw=True)

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
        self.avaliar_populacao(self.populacao)
        print("---- salvando ----")
        s.salvar_populacao(self.populacao, "populacao2")

        pass