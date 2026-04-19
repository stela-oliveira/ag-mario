from data.marioMain import mainMario


class Individuo:
    def __init__(self, cromossomo):
        self.cromossomo = cromossomo
        self.fitness = None

    def calcular_fitness(self, redraw=False):
        distance, time = mainMario(self.cromossomo, redraw)
        self.fitness = distance
    