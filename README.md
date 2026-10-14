# Game of Life, Langton's Ant & Glider Logic Gates

Python implementations of three classic cellular-automata topics, built as a course project for *Theory of Languages and Machines*:

1. **Conway's Game of Life** – finite and toroidal boundaries, a naive cell-by-cell engine and a fast convolution engine, and a loader for Plaintext (`.cells`) and RLE patterns.
2. **Langton's Ant** – the classic two-colour ant, multi-colour rule sets, and a pygame visualiser.
3. **Logic gates from gliders** – AND and NOT gates built from Game of Life gliders, illustrating that the Game of Life is Turing complete.

The common theme is **emergence**: very simple local rules produce complex global behaviour, and in the Game of Life's case even general-purpose computation.

## Table of contents

- [Repository layout](#repository-layout)
- [Installation](#installation)
- [Quick start](#quick-start)
- [Part 1 – Conway's Game of Life](#part-1--conways-game-of-life)
- [Part 2 – Langton's Ant](#part-2--langtons-ant)
- [Part 3 – Turing completeness with logic gates](#part-3--turing-completeness-with-logic-gates)
- [Tests](#tests)
- [Demos](#demos)
- [Included patterns and file formats](#included-patterns-and-file-formats)
- [Notes](#notes)
- [References](#references)

## Repository layout

```
.
├── conway.py                       # GameOfLife class + pattern parser (.cells / .rle)
├── langton.py                      # LangtonsAnt class
├── logic_gates.py                  # GliderLogicGates (AND / NOT)
├── pygame_viewer.py                # shared pygame renderer for Game of Life
├── pygame_gol.py                   # Game of Life window (AK-94 gun)
├── langton_pygame.py               # Langton's Ant window (command-line options)
│
├── test_conway_rules.py            # tests: blinker, survival/birth rules, boundaries
├── test_fast_convolution.py        # tests: fast vs. naive evolution + timing
├── test_logic_gates.py             # tests: AND / NOT truth tables
│
├── demo_blinker.py                 # demos (open a pygame window)
├── demo_glider.py
├── demo_gosper_gun.py
├── demo_load_pattern_file.py
├── demo_vacuum_gun.py
├── demo_large_cordership_gun.py
│
├── *.cells                         # pattern files (Plaintext format)
├── requirements.txt
└── README.md
```

Scripts named `test_*` run in the terminal and print `PASS` / `FAIL`. Scripts named `demo_*` open a pygame window. Pattern files are loaded by name relative to the working directory, so **run every script from the repository root**.

## Installation

Requires Python 3.8+.

```bash
git clone https://github.com/alimhmdabesi/conway-langton-automata.git
cd conway-langton-automata
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt  # numpy, scipy, pygame
```

## Quick start

```bash
python test_conway_rules.py --finite false   # verify the Game of Life rules
python demo_gosper_gun.py                    # watch a glider gun
python langton_pygame.py --steps 12000 --fps 500   # watch the ant build its highway
python test_logic_gates.py                   # AND / NOT truth tables
```

---

## Part 1 – Conway's Game of Life

Introduced by John Conway in 1970, the Game of Life is a two-dimensional cellular automaton. The world is a grid of cells that are either alive or dead, and every cell looks at its eight neighbours (Moore neighbourhood) to decide its state in the next generation. All cells update simultaneously.

### The four rules

| Cell | Live neighbours | Result |
|---|---|---|
| Alive | fewer than 2 | dies (underpopulation) |
| Alive | 2 or 3 | survives |
| Alive | more than 3 | dies (overpopulation) |
| Dead | exactly 3 | becomes alive (birth) |

### Implementation (`conway.py`)

The `GameOfLife` class keeps the grid in a NumPy array and offers:

- `GameOfLife(N=256, finite=False, fastMode=True)` – an `N × N` world.
- `evolve()` – advance one generation, using either engine depending on `fastMode`.
- `update_grid_fast(grid)` – the convolution engine.
- `getStates()` / `getGrid()` – the current grid (1 = alive, 0 = dead).
- `insertBlinker(index)`, `insertGlider(index)`, `insertGliderGun(index)` – built-in patterns placed at `(row, col)`.
- `insertFromFile(filename, index)` – load a `.cells` or `.rle` pattern.

**Boundary modes**

- **Finite** (`finite=True`): cells outside the grid are always dead, so a corner cell has only 3 neighbours instead of 8.
- **Toroidal** (`finite=False`): opposite edges are connected, so leaving through the right edge re-enters on the left, and likewise top/bottom. The grid behaves like the surface of a torus.

**Two evolution engines**

- *Naive (cell-by-cell)*: nested loops count the neighbours of every cell. It is `O(N²)` per generation and becomes very slow for large grids (N > 1024).
- *Fast (convolution)*: `scipy.signal.convolve2d` counts all neighbours at once with a 3×3 kernel (ones everywhere except a zero in the centre), and the rules are applied in vectorised form. Both boundary modes are supported and the result is identical to the naive engine. It is typically one to two orders of magnitude faster; for example, 50 generations on a random 256×256 grid took about 10 s with the naive engine and about 0.2 s with the fast one in a test run.

**Important patterns**

- **Blinker** – an oscillator of period 2 (a line of three cells flips between horizontal and vertical).
- **Glider** – a small pattern that travels diagonally at speed c/4 (one cell every 4 generations) while keeping its shape. Because it moves without changing, it is ideal for carrying signals, and gliders can implement logic when they collide with each other or with other patterns.
- **Glider gun** – a pattern that periodically emits gliders. The best known is the **Gosper glider gun**, the first one discovered.

**Pattern loading (`parse_pattern`)**

`parse_pattern(filepath)` returns `(width, height, live_cells)` and supports Plaintext (`.cells`) and RLE (`.rle`) files; the format is detected automatically. See [file formats](#included-patterns-and-file-formats).

### Using the module

```python
import conway
from pygame_viewer import run_pygame_life

life = conway.GameOfLife(N=64, finite=False, fastMode=True)
life.insertGlider((0, 0))
life.insertFromFile("ak94 gun.cells", (10, 10))
life.evolve()                                   # one generation
grid = life.getGrid()                           # NumPy array
run_pygame_life(life, cell_scale=10, fps=20, max_frames=300)
```

---

## Part 2 – Langton's Ant

Langton's Ant, introduced by Chris Langton in 1986, is a two-dimensional Turing machine. The ant has a position, a heading (`U`, `R`, `D`, `L`) and walks over a grid of coloured cells.

### Rules (two colours)

- On a **white** cell: turn the cell black, turn 90° **right**, move one cell forward.
- On a **black** cell: turn the cell white, turn 90° **left**, move one cell forward.

### Behaviour

- **Chaotic phase** – during the first several thousand steps the ant moves irregularly and leaves an asymmetric, seemingly random pattern.
- **The highway** – after roughly 10,000 steps the ant suddenly locks into a repeating 104-step cycle and travels diagonally forever, building a "highway". The transition from chaos to order is a striking example of emergence.

### Multi-colour ants

Rules are a dictionary mapping the current colour to `(next_colour, turn)`. With more than two colours, many different rule sets give intricate, often symmetric patterns.

```python
from langton import LangtonsAnt

rules = {0: (1, "R"), 1: (0, "L")}      # classic ant
ant = LangtonsAnt(200, (100, 100), rules)   # (grid size, (row, col), rules)
for _ in range(11000):
    ant.step()
grid = ant.get_states()
```

The ant moves with toroidal wrapping at the grid borders. Other methods: `get_current_position()` and `reset()`.

### Visualiser (`langton_pygame.py`)

```bash
python langton_pygame.py                                    # classic ant, defaults
python langton_pygame.py --steps 12000 --fps 500            # run into the highway
python langton_pygame.py --multi-color --steps 2000         # four-colour rule set
python langton_pygame.py --size 300 --cell-scale 4 --steps 10000
```

| Option | Default | Meaning |
|---|---|---|
| `--size` | 200 | grid size (N × N) |
| `--row`, `--col` | centre | starting position |
| `--cell-scale` | 6 | pixels per cell |
| `--fps` | 60 | frames per second |
| `--steps` | unlimited | maximum number of steps |
| `--multi-color` | off | use a four-colour rule set instead of the two-colour one |

---

## Part 3 – Turing completeness with logic gates

A system is Turing complete if it can compute anything a Turing machine can. It is enough to build a universal set of Boolean gates: AND and NOT together can express NAND, and NAND alone can build any Boolean function.

### Signals

Signals are encoded as **gliders**: a glider present means bit **1**, no glider means bit **0**.

### AND gate

Glider A travels from top to bottom and glider B from left to right, so their paths cross at a fixed point. If both are present they collide and leave a stable 2×2 block in the output region (output 1); if only one is present it passes through and the output stays empty (output 0).

| A | B | Output |
|---|---|---|
| 0 | 0 | 0 |
| 0 | 1 | 0 |
| 1 | 0 | 0 |
| 1 | 1 | 1 |

### NOT gate

A control glider is always fired toward the output region. If the input is 0 it arrives untouched (output 1). If the input is 1, the input glider is placed on a collision course and both gliders annihilate each other (output 0).

| Input | Output |
|---|---|
| 0 | 1 |
| 1 | 0 |

### Implementation (`logic_gates.py`)

```python
from logic_gates import GliderLogicGates

gates = GliderLogicGates()
gates.setup_and_gate(input_a_present=True, input_b_present=True)  # returns a GameOfLife grid
gates.run_and_gate(True, True)    # True
gates.run_not_gate(True)          # False
```

- `setup_and_gate(...)` / `setup_not_gate(...)` build a 35×35 finite Game of Life grid containing the required gliders.
- `run_and_gate(a, b)` / `run_not_gate(a)` set up the grid, evolve it for 40 generations and return the gate result.

### Why this matters

With AND and NOT you can build NAND, then any Boolean function, combinational circuits (adders, multipliers), sequential circuits (flip-flops, memory) and, in principle, a complete computer inside the Game of Life. Hence Conway's Game of Life is Turing complete: despite four trivial rules, it can run any computable algorithm.

---

## Tests

All tests run in the terminal without opening a window. They are plain scripts, so run them with `python` (not `pytest`).

| Command | What it checks |
|---|---|
| `python test_conway_rules.py --finite true` | Blinker has period 2 (vertical → horizontal → vertical), survival and birth rules hold, and the finite boundary behaves correctly. |
| `python test_conway_rules.py --finite false` | Same checks, plus cells wrap around the edges in toroidal mode. |
| `python test_fast_convolution.py --finite true` | On a random 256×256 grid over 50 generations, fast mode gives exactly the same grid as naive mode (finite boundary); prints both timings. |
| `python test_fast_convolution.py --finite false` | Same comparison with toroidal boundary. |
| `python test_logic_gates.py` | Truth tables of the AND and NOT gates. |

Expected final lines: `PART 1a TEST PASSED`, `PASS: Fast implementation is correct.`, `ALL LOGIC GATES TESTS PASSED`.

## Demos

These open a pygame window; close the window to stop. To try another pattern, edit the `insertFromFile(...)` line in the script.

| Command | Shows |
|---|---|
| `python demo_blinker.py` | Blinker – quick check that the rules work. |
| `python demo_glider.py --finite true` / `false` | A glider in the corner, to compare finite and toroidal worlds. |
| `python demo_gosper_gun.py` | Gosper glider gun emitting an endless stream of gliders. |
| `python demo_load_pattern_file.py` | Loads `dragon spaceship.cells` from a file. |
| `python demo_vacuum_gun.py` | Vacuum gun pattern. |
| `python demo_large_cordership_gun.py` | 4096×4096 grid with a cropped viewport (3-engine Cordership gun). |
| `python pygame_gol.py` | AK-94 gun on a 100×100 grid. |
| `python langton_pygame.py` | Langton's Ant (see [options](#visualiser-langton_pygamepy)). |

## Included patterns and file formats

| File | Pattern |
|---|---|
| `ak94 gun.cells` | AK-94, smallest known true period-94 gun |
| `vacuumgun gun.cells` | Vacuum gun |
| `dragon spaceship.cells` | Dragon, first c/6 spaceship |
| `7enginecordership spaceship.cells` | 7-engine Cordership |
| `3enginecordership gun 279x258.cells` | 3-engine Cordership gun |
| `stargate oscillator.cells` | Star gate |

These patterns come from the Game of Life community; the header inside each file names the original author (see also [LifeWiki](https://conwaylife.com/wiki)).

**Plaintext (`.cells`)** – one row per line, `O`/`o` for a live cell, `.` for a dead cell, lines starting with `!` are comments.

```
! Glider
.O.
..O
OOO
```

**RLE (`.rle`)** – compact run-length encoding. The header gives the size (`x=3, y=3`), then `o` = alive, `b` = dead, a number repeats the next symbol (`3o` = `ooo`), `$` ends a row and `!` ends the pattern.

```
x = 3, y = 3, rule = B3/S23
bob$2bo$3o!
```

## Notes

- `run_and_gate` and `run_not_gate` build the glider configuration and evolve it for 40 generations, but the value they return is computed logically from the inputs; it is not read back from the final grid.
- Fast mode relies on `scipy.signal.convolve2d`; for small grids the naive engine is perfectly adequate.

## References

- C. Moore and S. Mertens, *The Nature of Computation*, Oxford University Press, 2011.
- [LifeWiki](https://conwaylife.com/wiki)
- Wikipedia: *Conway's Game of Life*, *Langton's ant*, *Turing completeness*
