# -*- coding: utf-8 -*-
"""
Game of Life simple script for checking init states and checking if the evolution is
implemented correctly.
"""

import argparse
import conway
from pygame_viewer import run_pygame_life


N = 64
CELL_SCALE = 10


def str_to_bool(value):
    """
    Convert command line string to boolean.
    """
    if isinstance(value, bool):
        return value

    value = value.lower()

    if value in ("true", "1", "yes", "y"):
        return True

    if value in ("false", "0", "no", "n"):
        return False

    raise argparse.ArgumentTypeError(
        "Boolean value expected: true/false"
    )


def main():

    parser = argparse.ArgumentParser(
        description="Conway Game of Life Glider Viewer"
    )

    parser.add_argument(
        "--finite",
        type=str_to_bool,
        default=True,
        help="World mode: true=finite, false=infinite(toroidal wrapping)"
    )

    args = parser.parse_args()


    print("=" * 50)
    print("Game of Life - Glider Check")
    print("=" * 50)


    if args.finite:
        print("Mode: FINITE")
    else:
        print("Mode: INFINITE / TOROIDAL")


    life = conway.GameOfLife(
        N=N,
        finite=args.finite
    )


    # Place glider in corner to test wrapping
    life.insertGlider((0, 0))


    run_pygame_life(
        life,
        cell_scale=CELL_SCALE,
        fps=8,
        max_frames=300,
        title="Game of Life - Glider Check"
    )


if __name__ == "__main__":
    main()