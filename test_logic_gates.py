# -*- coding: utf-8 -*-

"""
Test file for Conway Game of Life Logic Gates.

Checks:
- AND Gate truth table
- NOT Gate truth table
"""


from logic_gates import GliderLogicGates



def test_and_gate():

    print("=" * 60)
    print("Testing AND Gate")
    print("=" * 60)


    gate = GliderLogicGates()


    tests = [

        (False, False, False),
        (False, True,  False),
        (True,  False, False),
        (True,  True,  True),

    ]


    passed = True


    for a, b, expected in tests:

        result = gate.run_and_gate(a, b)


        print(
            f"AND({int(a)},{int(b)}) "
            f"=> Output: {int(result)} "
            f"Expected: {int(expected)}"
        )


        if result != expected:
            passed = False



    print()


    if passed:
        print("PASS: AND Gate")
    else:
        print("FAIL: AND Gate")


    return passed





def test_not_gate():

    print("=" * 60)
    print("Testing NOT Gate")
    print("=" * 60)


    gate = GliderLogicGates()


    tests = [

        (False, True),
        (True, False),

    ]


    passed = True


    for a, expected in tests:


        result = gate.run_not_gate(a)


        print(
            f"NOT({int(a)}) "
            f"=> Output: {int(result)} "
            f"Expected: {int(expected)}"
        )


        if result != expected:
            passed = False



    print()


    if passed:
        print("PASS: NOT Gate")
    else:
        print("FAIL: NOT Gate")


    return passed





def main():

    print("\n")
    print("#" * 60)
    print(" Conway Logic Gates Test ")
    print("#" * 60)


    and_ok = test_and_gate()


    print()


    not_ok = test_not_gate()



    print("\n")
    print("=" * 60)


    if and_ok and not_ok:
        print("ALL LOGIC GATES TESTS PASSED")
    else:
        print("LOGIC GATES TEST FAILED")


    print("=" * 60)





if __name__ == "__main__":
    main()