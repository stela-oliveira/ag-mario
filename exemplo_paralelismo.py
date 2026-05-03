import os
os.environ["SDL_VIDEODRIVER"] = "dummy"
from random import randint, random, uniform
import numpy as np
import os.path
import os
import errno
import csv
import sys
import pygame as pg
import asyncio
from concurrent.futures import ProcessPoolExecutor
from data import marioMain

MIN_INSTRUCTIONS = 20
MAX_INSTRUCTIONS = 2000
MIN_TIME = 50
MAX_TIME = 400
N_COMMANDS = 6

N_GENERATIONS = 20
POPULATION_SIZE = 100
TOURNAMENT_SIZE = 2
ELITISM_SIZE = 1
P_TOUR = 0.7
P_CROSSOVER = 0.5
P_MUTATE = 20

MAX_DISTANCE = 100
SAVE_FREQUENCY = 1
POPULATION_FOLDER = 'populations'

DRAW_FRAMES = False  # ⚠️ IMPORTANTE: desativado para paralelismo


def initialize_population():
    population = []
    for i in range(POPULATION_SIZE):
        n_instructions = randint(MIN_INSTRUCTIONS, MAX_INSTRUCTIONS)
        chromosome = []
        for j in range(n_instructions):
            random_command = randint(1, N_COMMANDS)
            random_time = randint(MIN_TIME, MAX_TIME)
            chromosome.append(random_command)
            chromosome.append(random_time)
        population.append(chromosome)
    return population


def get_fitness(distance, time):
    return distance


def tournament_select(fitness_list):
    population_size = len(fitness_list)
    indices = np.random.randint(population_size, size=TOURNAMENT_SIZE)
    fitness_tmp = fitness_list[indices]
    sorting = fitness_tmp.argsort()
    indices = indices[sorting]

    not_selected = True
    tournament_counter = 1

    while not_selected:
        if random() < P_TOUR or tournament_counter == TOURNAMENT_SIZE:
            index_selected = indices[0]
            not_selected = False
        else:
            indices = np.delete(indices, 0)
        tournament_counter += 1

    return index_selected


def crossover(chromosome_1, chromosome_2):
    length_c_1 = len(chromosome_1)
    length_c_2 = len(chromosome_2)

    split_1 = 2 * randint(1, length_c_1 // 2 - 2)
    split_2 = 2 * randint(split_1 // 2 + 1, length_c_1 // 2 - 1)
    split_3 = 2 * randint(1, length_c_2 // 2 - 2)
    split_4 = 2 * randint(split_3 // 2 + 1, length_c_2 // 2 - 1)

    c_1_part_1 = chromosome_1[0:split_1]
    c_1_part_2 = chromosome_1[split_1:split_2]
    c_1_part_3 = chromosome_1[split_2:length_c_1]

    c_2_part_1 = chromosome_2[0:split_3]
    c_2_part_2 = chromosome_2[split_3:split_4]
    c_2_part_3 = chromosome_2[split_4:length_c_2]

    new_c_1 = [c_1_part_1, c_2_part_2, c_1_part_3]
    new_c_2 = [c_2_part_1, c_1_part_2, c_2_part_3]

    new_c_1 = [value for part in new_c_1 for value in part]
    new_c_2 = [value for part in new_c_2 for value in part]

    return new_c_1, new_c_2


def mutate(chromosome):
    for i in range(len(chromosome)):
        if uniform(0, 1) < P_MUTATE:
            if i % 2 == 0:
                chromosome[i] = randint(1, N_COMMANDS)
            else:
                chromosome[i] = randint(MIN_TIME, MAX_TIME)
    return chromosome


def perform_elitism(population, best_chromosome):
    for i in range(ELITISM_SIZE):
        population[i] = best_chromosome
    return population


# 🔥 Função executada em paralelo (precisa estar no topo!)
def run_individual(chromosome):
    distance, time = marioMain.mainMario(chromosome, redraw=False)
    return distance, time


# 🔥 Execução paralela
async def evaluate_population_async(population):
    loop = asyncio.get_event_loop()

    # Ajuste conforme número de núcleos
    with ProcessPoolExecutor(max_workers=10) as executor:
        tasks = [
            loop.run_in_executor(executor, run_individual, chromosome)
            for chromosome in population
        ]

        results = await asyncio.gather(*tasks)

    return results


def main():
    print('- Enter a name of the population')
    population_name = input()

    file_path = os.path.join(POPULATION_FOLDER, f'{population_name}.txt')

    if os.path.isfile(file_path):
        population = []
        with open(file_path, 'r') as csv_file:
            reader = csv.reader(csv_file, delimiter=';')
            for row in reader:
                population.append(list(map(int, row)))
    else:
        population = initialize_population()

    best_fitness = 0
    best_chromosome = []

    for generation in range(N_GENERATIONS):
        print(f'\n=== Generation {generation} ===')

        # 🔥 Paralelismo aqui
        results = asyncio.run(evaluate_population_async(population))

        fitness_list = []

        for i, (distance, time) in enumerate(results):
            print(f'Individual {i} -> distance: {distance}')
            fitness = get_fitness(distance, time)
            fitness_list.append(fitness)

            if fitness > best_fitness:
                best_chromosome = population[i]
                best_fitness = fitness

        fitness_list = np.array(fitness_list)

        tmp_population = []

        for i in range(0, POPULATION_SIZE, 2):
            index_1 = tournament_select(fitness_list)
            index_2 = tournament_select(fitness_list)

            chromosome_1 = population[index_1]
            chromosome_2 = population[index_2]

            if random() < P_CROSSOVER:
                chromosome_1, chromosome_2 = crossover(chromosome_1, chromosome_2)

            tmp_population.append(chromosome_1)
            tmp_population.append(chromosome_2)

        for i in range(len(tmp_population)):
            tmp_population[i] = mutate(tmp_population[i])

        population = perform_elitism(tmp_population, best_chromosome)

        if generation % SAVE_FREQUENCY == 0:
            if os.path.isfile(file_path):
                os.remove(file_path)

            if not os.path.exists(os.path.dirname(file_path)):
                try:
                    os.makedirs(os.path.dirname(file_path))
                except OSError as exc:
                    if exc.errno != errno.EEXIST:
                        raise

            with open(file_path, 'w', newline='') as csv_file:
                writer = csv.writer(csv_file, delimiter=';')
                for row in population:
                    writer.writerow(row)

    pg.quit()
    sys.exit()


if __name__ == "__main__":
    main()