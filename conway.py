"""
The Game of Life (GoL) module named in honour of John Conway

This module defines the classes required for the GoL simulation.
"""
import numpy as np
from scipy import signal


def parse_pattern(filepath):
    """
    Parse Conway Life pattern files.

    Supports:
        - Plaintext (.cells)
        - Run Length Encoded (.rle)

    Returns:
        (width, height, live_cells)
    """

    live_cells = []

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except (OSError, IOError):
        return 0, 0, []

    # -------------------------------------------------------
    # Detect file type
    # -------------------------------------------------------
    is_rle = any(line.lstrip().startswith("x") and "y" in line for line in lines)

    # =======================================================
    # RLE PARSER
    # =======================================================
    if is_rle:

        width = 0
        height = 0

        pattern = []

        for line in lines:

            line = line.strip()

            if not line:
                continue

            # comments
            if line.startswith("#"):
                continue

            # header
            if line.startswith("x"):
                parts = line.split(",")

                for part in parts:
                    part = part.strip()

                    if part.startswith("x"):
                        width = int(part.split("=")[1])

                    elif part.startswith("y"):
                        height = int(part.split("=")[1])

                continue

            pattern.append(line)

        pattern = "".join(pattern)

        row = 0
        col = 0
        count = ""

        for ch in pattern:

            if ch.isdigit():
                count += ch
                continue

            n = int(count) if count else 1
            count = ""

            if ch == "b":
                col += n

            elif ch == "o":
                for _ in range(n):
                    live_cells.append((row, col))
                    col += 1

            elif ch == "$":
                row += n
                col = 0

            elif ch == "!":
                break

        return width, height, live_cells

    # =======================================================
    # PLAINTEXT PARSER
    # =======================================================

    pattern_lines = []

    for line in lines:

        line = line.rstrip("\n")

        if not line:
            continue

        if line.startswith("!"):
            continue

        pattern_lines.append(line)

    height = len(pattern_lines)
    width = max((len(line) for line in pattern_lines), default=0)

    for r, line in enumerate(pattern_lines):
        for c, ch in enumerate(line):
            if ch in ("O", "o", "*"):
                live_cells.append((r, c))

    return width, height, live_cells


class GameOfLife:
    """
    Object for computing Conway's Game of Life (GoL) cellular machine/automata
    """

    def __init__(self, N=256, finite=False, fastMode=True):
        self.grid = np.zeros((N, N), np.uint)
        self.neighborhood = np.ones((3, 3), np.uint)
        self.neighborhood[1, 1] = 0
        self.finite = finite
        self.fastMode = fastMode
        self.aliveValue = 1
        self.deadValue = 0
        self.rows = N
        self.cols = N

    def getStates(self):
        return self.grid

    def getGrid(self):
        return self.getStates()

    def update_grid_fast(self, grid):
        """
        TODO: [Part 1e - Fast Convolution]

        Compute the next Game of Life generation using
        scipy.signal.convolve2d.
        """

        kernel = self.neighborhood

        if self.finite:
            neighbors = signal.convolve2d(
                grid,
                kernel,
                mode="same",
                boundary="fill",
                fillvalue=0
            )
        else:
            neighbors = signal.convolve2d(
                grid,
                kernel,
                mode="same",
                boundary="wrap"
            )

        next_grid = np.zeros_like(grid)

        # Survival
        next_grid[(grid == 1) & ((neighbors == 2) | (neighbors == 3))] = 1

        # Birth
        next_grid[(grid == 0) & (neighbors == 3)] = 1

        return next_grid

    def evolve(self):
        """
        TODO: [Part 1a - Core Rules]
        """
        if self.fastMode:
            self.grid = self.update_grid_fast(self.grid)
        else:
            # Slow cell-by-cell implementation
            new_grid = np.zeros_like(self.grid)
            for i in range(self.rows):
                for j in range(self.cols):
                    # Count neighbors
                    neighbors = 0
                    for di in [-1, 0, 1]:
                        for dj in [-1, 0, 1]:
                            if di == 0 and dj == 0:
                                continue
                            ni = (i + di) % self.rows if not self.finite else i + di
                            nj = (j + dj) % self.cols if not self.finite else j + dj
                            if 0 <= ni < self.rows and 0 <= nj < self.cols:
                                neighbors += self.grid[ni, nj]

                    # Apply rules
                    if self.grid[i, j] == 1:
                        if 2 <= neighbors <= 3:
                            new_grid[i, j] = 1
                    else:
                        if neighbors == 3:
                            new_grid[i, j] = 1
            self.grid = new_grid

    # Non-destructive insertion methods (only GliderGun requires fixing)
    def insertBlinker(self, index=(0, 0)):
        self.grid[index[0], index[1] + 1] = self.aliveValue
        self.grid[index[0] + 1, index[1] + 1] = self.aliveValue
        self.grid[index[0] + 2, index[1] + 1] = self.aliveValue

    def insertGlider(self, index=(0, 0)):
        self.grid[index[0], index[1] + 1] = self.aliveValue
        self.grid[index[0] + 1, index[1] + 2] = self.aliveValue
        self.grid[index[0] + 2, index[1]] = self.aliveValue
        self.grid[index[0] + 2, index[1] + 1] = self.aliveValue
        self.grid[index[0] + 2, index[1] + 2] = self.aliveValue

    def insertGliderGun(self, index=(0, 0)):
        """
        Insert the standard Gosper Glider Gun.
        """

        gun = [
            # Left block
            (5, 1), (5, 2),
            (6, 1), (6, 2),

            # Left oscillator
            (3, 13), (3, 14),
            (4, 12), (4, 16),
            (5, 11), (5, 17),
            (6, 11), (6, 15), (6, 17), (6, 18),
            (7, 11), (7, 17),
            (8, 12), (8, 16),
            (9, 13), (9, 14),

            # Right oscillator
            (1, 25),
            (2, 23), (2, 25),
            (3, 21), (3, 22),
            (4, 21), (4, 22),
            (5, 21), (5, 22),
            (6, 23), (6, 25),
            (7, 25),

            # Right block
            (3, 35), (3, 36),
            (4, 35), (4, 36),
        ]

        for dr, dc in gun:
            r = index[0] + dr
            c = index[1] + dc

            if 0 <= r < self.rows and 0 <= c < self.cols:
                self.grid[r, c] = self.aliveValue

    def insertFromFile(self, filename, index=(0, 0)):
        width, height, live_cells = parse_pattern(filename)
        for r, c in live_cells:
            target_r = index[0] + r
            target_c = index[1] + c
            if 0 <= target_r < self.rows and 0 <= target_c < self.cols:
                self.grid[target_r, target_c] = self.aliveValue