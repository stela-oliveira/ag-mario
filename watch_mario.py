#!/usr/bin/env python
"""Script para assistir o Mario jogando automaticamente com um chromosome"""
import pygame as pg

from data import marioMain

def main():
    while True:
        # adicione o cromossomo que deseja testar
        marioMain.mainMario(
            [11, 54, 11, 129, 10, 222, 8, 42, 0, 100, 10, 92, 9, 82, 11, 122, 9, 98, 11, 95, 0, 180, 11, 256, 8, 47, 11, 183, 9, 150, 10, 57, 8, 124, 9, 88, 10, 109, 8, 134, 10, 134, 0, 51, 11, 105, 8, 103, 11, 137, 2, 203, 0, 107, 10, 128, 8, 70, 11, 126, 9, 30, 11, 240, 11, 190, 8, 121, 9, 104, 11, 115, 8, 85, 11, 149, 9, 145, 10, 113, 11, 104, 8, 89, 8, 68, 10, 147], 
            redraw=True
        )

if __name__ == "__main__":
    main()