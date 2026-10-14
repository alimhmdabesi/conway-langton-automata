# -*- coding: utf-8 -*-

"""
Langton's Ant implementation.

Supports:
- Classic two-color Langton's Ant
- Multi-color rules
- Custom transition dictionary
"""


import numpy as np


class LangtonsAnt:

    DIRECTIONS = ["U", "R", "D", "L"]

    MOVES = {
        "U": (-1, 0),
        "R": (0, 1),
        "D": (1, 0),
        "L": (0, -1),
    }


    def __init__(
            self,
            size,
            start_position,
            rules
    ):
        """
        Initialize Langton's Ant.

        Parameters:
            size:
                Grid size (NxN)

            start_position:
                Tuple(row,col)

            rules:
                Dictionary:
                {
                    current_color:
                    (
                        next_color,
                        turn
                    )
                }

                Example:
                {
                    0:(1,"R"),
                    1:(0,"L")
                }
        """

        self.size = size

        # numpy grid for pygame compatibility
        self.grid = np.zeros(
            (size, size),
            dtype=int
        )


        self.position = (
            int(start_position[0]),
            int(start_position[1])
        )


        # initial direction
        self.direction = "U"


        # transition rules
        self.rules = rules



    def turn_right(self):
        """
        Rotate ant 90 degrees clockwise.
        """

        index = self.DIRECTIONS.index(
            self.direction
        )

        self.direction = self.DIRECTIONS[
            (index + 1) % 4
        ]



    def turn_left(self):
        """
        Rotate ant 90 degrees counter-clockwise.
        """

        index = self.DIRECTIONS.index(
            self.direction
        )

        self.direction = self.DIRECTIONS[
            (index - 1) % 4
        ]



    def move_forward(self):
        """
        Move one cell forward.
        """

        dr, dc = self.MOVES[
            self.direction
        ]

        r, c = self.position

        r += dr
        c += dc


        # wrap around boundaries
        r %= self.size
        c %= self.size


        self.position = (r, c)



    def step(self):
        """
        Execute one Langton ant step.

        Rules:
        1- Read current cell color
        2- Change color
        3- Rotate
        4- Move
        """


        r, c = self.position


        current_color = int(
            self.grid[r, c]
        )


        if current_color not in self.rules:
            raise ValueError(
                f"No rule defined for color {current_color}"
            )


        next_color, rotation = self.rules[
            current_color
        ]


        # change cell color
        self.grid[r, c] = next_color



        # rotate

        if rotation == "R":

            self.turn_right()

        elif rotation == "L":

            self.turn_left()

        else:

            raise ValueError(
                "Rotation must be R or L"
            )


        # move

        self.move_forward()



    def get_states(self):
        """
        Return current grid state.

        Must be numpy array
        for pygame viewer.
        """

        return self.grid



    def get_current_position(self):
        """
        Return current ant position.
        """

        return self.position



    def reset(self):
        """
        Reset simulation.
        """

        self.grid.fill(0)

        self.position = (
            self.size // 2,
            self.size // 2
        )

        self.direction = "U"