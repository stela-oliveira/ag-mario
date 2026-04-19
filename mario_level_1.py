#!/usr/bin/env python


import random
import sys
import pygame as pg
from data.marioMain import mainMario
import cProfile


if __name__=='__main__':
    # Chromosome vazio para jogo manual (controle do jogador)

    chromosome = []

    distance, time = mainMario(chromosome, redraw=True)
    print("Tempo: ", time)
    pg.quit()
    sys.exit()
























