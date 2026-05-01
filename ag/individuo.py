from data.marioMain import mainMario
import uuid


class Individuo:
    def __init__(self, cromossomo: list[int]):
        self.cromossomo: list[int] = cromossomo
        self.fitness: int | float | None = None
        self.uuid = uuid.uuid4()

    def calcular_fitness(self, redraw=False):
        distance, time = mainMario(self.cromossomo, redraw)
        self.fitness = distance
        return self.fitness
    