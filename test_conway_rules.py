import argparse
import numpy as np
import conway


def print_grid(grid):
    for row in grid:
        print(" ".join(map(str, row)))
    print()


def test_blinker_rules(finite=True):
    print("=" * 60)
    print("Testing Part 1a - Conway Core Rules")
    print("=" * 60)

    print("Mode:",
          "FINITE" if finite else "TOROIDAL")

    game = conway.GameOfLife(
        N=20,
        finite=finite,
        fastMode=False
    )

    # Blinker in center
    game.insertBlinker((10, 10))

    initial = game.grid.copy()

    print("\nGeneration 0")
    print_grid(game.grid)

    # Generation 1
    game.evolve()

    print("Generation 1")
    print_grid(game.grid)

    expected_gen1 = np.zeros((20, 20), dtype=np.uint8)

    # horizontal blinker
    expected_gen1[11, 10] = 1
    expected_gen1[11, 11] = 1
    expected_gen1[11, 12] = 1

    if np.array_equal(game.grid, expected_gen1):
        print("PASS: Survival and Reproduction rules")
    else:
        print("FAIL: Core rules incorrect")
        return False


    # Generation 2
    game.evolve()

    print("Generation 2")
    print_grid(game.grid)

    if np.array_equal(game.grid, initial):
        print("PASS: Blinker period = 2")
    else:
        print("FAIL: Blinker period incorrect")
        return False

    return True



def test_wrapping():
    print("=" * 60)
    print("Testing Boundary Conditions")
    print("=" * 60)


    # Test finite boundary
    finite_game = conway.GameOfLife(
        N=5,
        finite=True,
        fastMode=False
    )


    # vertical blinker at top-left corner
    finite_game.insertBlinker((0, 0))

    print("\nFinite=True initial")
    print_grid(finite_game.grid)


    finite_game.evolve()

    print("Finite=True generation 1")
    print_grid(finite_game.grid)



    # Test toroidal boundary

    torus_game = conway.GameOfLife(
        N=5,
        finite=False,
        fastMode=False
    )


    torus_game.insertBlinker((0, 0))


    print("Toroidal initial")
    print_grid(torus_game.grid)


    torus_game.evolve()


    print("Toroidal generation 1")
    print_grid(torus_game.grid)



    if np.sum(torus_game.grid) > 0:
        print("PASS: Toroidal wrapping works")
        return True

    else:
        print("FAIL: Toroidal wrapping failed")
        return False



def main():

    parser = argparse.ArgumentParser(
        description="Test Conway Game of Life Part 1a"
    )

    parser.add_argument(
        "--finite",
        type=str,
        default="true",
        help="Boundary mode: true or false"
    )

    args = parser.parse_args()


    finite = args.finite.lower() == "true"


    result1 = test_blinker_rules(finite)

    result2 = test_wrapping()


    print("\n" + "=" * 60)

    if result1 and result2:
        print("PART 1a TEST PASSED")
    else:
        print("PART 1a TEST FAILED")

    print("=" * 60)



if __name__ == "__main__":
    main()