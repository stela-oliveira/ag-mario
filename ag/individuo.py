from data.marioMain import mainMario
import uuid


class Individuo:
    def __init__(self, cromossomo):
        self.cromossomo = cromossomo
        self.fitness = None
        self.uuid = uuid.uuid4()

    def calcular_fitness(self, redraw=False):
        distance, time = mainMario(self.cromossomo, redraw)
        self.fitness = distance
        return self.fitness
    