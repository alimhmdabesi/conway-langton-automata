import argparse
import time
import numpy as np
import conway


def str2bool(v):
    if isinstance(v, bool):
        return v

    if v.lower() in ("true", "1", "yes", "y"):
        return True

    if v.lower() in ("false", "0", "no", "n"):
        return False

    raise argparse.ArgumentTypeError("Boolean value expected.")


def test_fast_convolution(finite):

    N = 256

    slow = conway.GameOfLife(
        N=N,
        finite=finite,
        fastMode=False
    )

    fast = conway.GameOfLife(
        N=N,
        finite=finite,
        fastMode=True
    )

    np.random.seed(42)

    initial_grid = np.random.randint(
        0,
        2,
        (N, N),
        dtype=np.uint
    )

    slow.grid = initial_grid.copy()
    fast.grid = initial_grid.copy()

    # Slow timing
    start = time.time()

    for _ in range(50):
        slow.evolve()

    slow_time = time.time() - start

    # Fast timing
    start = time.time()

    for _ in range(50):
        fast.evolve()

    fast_time = time.time() - start

    print(f"Boundary Mode : {'Finite' if finite else 'Toroidal'}")
    print(f"Slow Mode     : {slow_time:.3f} s")
    print(f"Fast Mode     : {fast_time:.3f} s")

    if np.array_equal(slow.grid, fast.grid):
        print("PASS: Fast implementation is correct.")
    else:
        print("FAIL: Results are different.")


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Test Game of Life fast convolution."
    )

    parser.add_argument(
        "--finite",
        type=str2bool,
        default=False,
        help="Boundary mode: true (finite) or false (toroidal)"
    )

    args = parser.parse_args()

    test_fast_convolution(args.finite)