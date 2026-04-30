import individuo

class Populacao:
    def __init__(self, individuos: list[individuo.Individuo] = []):
        self.individuos : list[individuo.Individuo] = individuos

    def add_individuo(self, individuo: individuo.Individuo):
        self.individuos.append(individuo)

    def pegar_melhor(self):
        if not self.individuos:
            return None
        melhor = self.individuos[0]
        for individuo in self.individuos:
            if individuo.fitness is not None:
                if melhor.fitness is None or individuo.fitness > melhor.fitness:
                    melhor = individuo
        return melhor

    def ordenar_por_fitness(self):
        self.individuos.sort(key=lambda x: x.fitness if x.fitness is not None else -float('inf'), reverse=True)

    