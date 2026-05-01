from random import randint
import random

import individuo
import serializer as s
import populacao as p

class AlgoritmoGenetico: 
    def __init__(self, tamanho_populacao, tamanho_cromossomo):
        self.tamanho_populacao = tamanho_populacao
        self.tamanho_cromossomo = tamanho_cromossomo
        self.populacao = p.Populacao()

    def gerar_cromossomo(self) -> list[int]:
        cromossomo = []
        for _ in range(self.tamanho_cromossomo):
            cromossomo.append(random.randint(0, 6))
            cromossomo.append(random.randint(50, 200))
        return cromossomo

    def inicializar_populacao(self, cromossomo_base: list[int] | None = None):
        for _ in range(self.tamanho_populacao):
            if cromossomo_base:
                # Calcula um ponto de corte seguro para não estourar o randint
                limite_corte = max(1, self.tamanho_cromossomo // 4)
                # Corta o final do cromossomo base (ex: retira os últimos 1 a N movimentos)
                local_corte = len(cromossomo_base) - (randint(1, limite_corte) * 2)
                cromossomo_cortado = cromossomo_base[:local_corte]
                
                # Gera novos movimentos apenas para preencher/estender um pouco
                novos_movimentos = self.gerar_cromossomo()
                # Mantém o tamanho sob controle ou estende levemente em vez de dobrar
                self.populacao.add_individuo(individuo.Individuo([*cromossomo_cortado, *novos_movimentos]))
            else:
                cromossomo = self.gerar_cromossomo()
                self.populacao.add_individuo(individuo.Individuo(cromossomo))

    def avaliar_populacao(self, populacao: p.Populacao):
        for ind in populacao.individuos:
            if ind.fitness is None:
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

        cromossomo_do_melhor_individuo: list[int] = self.populacao.pegar_melhor().cromossomo
        fitness_do_melhor_individuo: int = self.populacao.pegar_melhor().fitness

        print("---------")
        print("Melhor cromossomo")
        print(cromossomo_do_melhor_individuo)
        print("Fitness: ")
        print(fitness_do_melhor_individuo)

        QUANTIDADE_CICLOS = 20
        for i in range(QUANTIDADE_CICLOS):
            print("Ciclo ", i)
            
            # Limpa a população para o novo ciclo (mantendo apenas o melhor se desejar elitismo)
            melhor_atual = self.populacao.pegar_melhor()
            self.populacao.limpar()
            
            # Opcional: Elitismo (mantém o melhor indivíduo sem alterações)
            if melhor_atual:
                self.populacao.add_individuo(melhor_atual)
            
            self.inicializar_populacao(cromossomo_do_melhor_individuo)
            self.avaliar_populacao(self.populacao)

            melhor_do_ciclo = self.populacao.pegar_melhor()
            cromossomo_do_melhor_individuo = melhor_do_ciclo.cromossomo
            fitness_do_melhor_individuo = melhor_do_ciclo.fitness

            print("---------")
            print("Melhor cromossomo")
            print(cromossomo_do_melhor_individuo)
            print("Fitness: ")
            print(fitness_do_melhor_individuo)




        # print("---- salvando ----")
        # s.salvar_populacao(self.populacao, "populacao2")

        pass