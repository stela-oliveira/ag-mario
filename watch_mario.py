#!/usr/bin/env python
"""Script para assistir o Mario jogando automaticamente com um chromosome"""

import csv
import sys
import pygame as pg
from data import marioMain

POPULATION_FOLDER = 'populations'

def load_population(population_name):
    file_path = f"{POPULATION_FOLDER}/{population_name}.txt"
    population = []
    with open(file_path, 'r') as csv_file:
        reader = csv.reader(csv_file, delimiter=';')
        for row in reader:
            population.append(list(map(int, row)))
    return population


def main():
    if len(sys.argv) > 1:
        population_name = sys.argv[1]
    else:
        print("Nome da população:", end=" ", flush=True)
        population_name = input().strip()
    
    print(f"\nCarregando população: {population_name}")
    population = load_population(population_name)
    print(f"População carregada com {len(population)} indivíduos\n")
    
    if len(sys.argv) > 2:
        individual_idx = int(sys.argv[2])
    else:
        print(f"Qual indivíduo testar? (0-{len(population)-1}):", end=" ", flush=True)
        individual_idx = int(input().strip())
    
    chromosome = population[individual_idx]
    
    print(f"\n{'='*60}")
    print(f"▶ Assistindo indivíduo {individual_idx}")
    print(f"  Chromosome length: {len(chromosome)} genes ({len(chromosome)//2} comandos)")
    print(f"  Primeiros comandos: {chromosome[:8]}")
    print(f"{'='*60}\n")
    
    # Redesenha os frames para ver o Mario jogando
    distance, time = marioMain.mainMario(chromosome, redraw=True)
    
    print(f"\n{'='*60}")
    print(f"Distância percorrida: {distance}")
    print(f"Tempo: {time}ms")
    print(f"{'='*60}")
    
    pg.quit()
    sys.exit()

if __name__ == "__main__":
    main()
