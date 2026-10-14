# -*- coding: utf-8 -*-
"""
Game of life simple script for checking init states and checking if the evolution is
implemented correctly.
"""
import conway
from pygame_viewer import run_pygame_life

N = 64
CELL_SCALE = 10


def main():
	"""Show the glider evolution in a pygame window."""
	life = conway.GameOfLife(N=64, finite=True, fastMode=True)
	life.insertGliderGun((0,0))     # Gosper glider gun consists of two queen bee shuttles stabilized by two blocks.
	run_pygame_life(life, cell_scale=CELL_SCALE, fps=8, max_frames=300, title="Game of Life - Glider Check")


if __name__ == "__main__":
	main()
