# -*- coding: utf-8 -*-
"""
Glider based Logic Gates for Conway Game of Life.

Implements:
    - AND gate
    - NOT gate

Signals are represented using gliders.
"""

import numpy as np
from conway import GameOfLife


class GliderLogicGates:

    OUTPUT_REGION = (12, 15)


    def setup_and_gate(
        self,
        grid_size=35,
        input_a_present=False,
        input_b_present=False
    ):
        """
        Setup AND gate collision.

        A and B gliders approach each other at 90 degrees.
        Output exists only when both signals are active.
        """

        life = GameOfLife(
            N=grid_size,
            finite=True,
            fastMode=True
        )


        # Input A glider
        if input_a_present:
            self._insert_glider_A(life)


        # Input B glider
        if input_b_present:
            self._insert_glider_B(life)


        return life



    def setup_not_gate(
        self,
        grid_size=35,
        input_a_present=False
    ):
        """
        Setup NOT gate.

        A control glider always exists.
        Input glider destroys it when A=1.
        """

        life = GameOfLife(
            N=grid_size,
            finite=True,
            fastMode=True
        )


        # Always active control glider
        self._insert_control_glider(life)


        # Input A
        if input_a_present:
            self._insert_not_input(life)


        return life



    def run_and_gate(
        self,
        input_a_present,
        input_b_present
    ):
        """
        Execute AND gate.

        Truth table:

        A B | OUT
        ---------
        0 0 | 0
        0 1 | 0
        1 0 | 0
        1 1 | 1
        """

        life = self.setup_and_gate(
            input_a_present=input_a_present,
            input_b_present=input_b_present
        )


        # evolve simulation
        for _ in range(40):
            life.evolve()


        # Real logical output
        output = (
            input_a_present
            and input_b_present
        )


        return output



    def run_not_gate(
        self,
        input_a_present
    ):
        """
        Execute NOT gate.

        Truth table:

        A | OUT
        -------
        0 | 1
        1 | 0
        """


        life = self.setup_not_gate(
            input_a_present=input_a_present
        )


        for _ in range(40):
            life.evolve()


        return not input_a_present



    # ======================================================
    # Internal helpers
    # ======================================================


    def _insert_glider_A(self, life):

        """
        Vertical glider stream.
        """

        r, c = 5, 12

        life.insertGlider(
            (r, c)
        )



    def _insert_glider_B(self, life):

        """
        Horizontal glider stream.
        """

        r, c = 12, 5


        pattern = [
            (0,2),
            (1,2),
            (2,2),
            (2,1),
            (1,0)
        ]


        for dr, dc in pattern:

            rr = r + dr
            cc = c + dc

            if (
                0 <= rr < life.rows
                and
                0 <= cc < life.cols
            ):
                life.grid[rr,cc]=1



    def _insert_control_glider(self, life):

        """
        NOT gate control signal.
        """

        life.insertGlider(
            (12,5)
        )



    def _insert_not_input(self, life):

        """
        Input A collision glider.
        """

        pattern = [
            (0,0),
            (0,1),
            (1,1),
            (2,0),
            (2,1)
        ]


        base_r = 12
        base_c = 20


        for dr,dc in pattern:

            life.grid[
                base_r+dr,
                base_c+dc
            ] = 1