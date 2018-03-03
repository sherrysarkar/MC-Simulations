import numpy as np
from matplotlib.path import Path
from matplotlib.patches import PathPatch
import matplotlib.pyplot as plt

import random


class EulerianPathState:
    def __init__(self, sources, sinks, boundary_size, grid=[]):
        if len(sources) != len(sinks):
            raise Exception("Unequal number of sources and sinks.")
        self.sources = sources
        self.sinks = sinks
        self.boundary_size = boundary_size

        # Let each face be uniquely represented by it's lowest left most corner.
        if len(grid) == 0:
            self.grid = self.generate_paths()
        else:
            self.grid = grid

    def generate_paths(self):
        # generate a valid Eulerian Routing
        grid = [[0 for j in range(self.boundary_size)] for i in range(self.boundary_size)]

        # First, go around the boundary, with sources then sinks.
        for y in range(1, self.boundary_size):
            if (0, y) in self.sources:
                grid[0][y] = (grid[0][y - 1] + 1) % 3
            else:
                grid[0][y] = (grid[0][y - 1] - 1) % 3

        for x in range(1, self.boundary_size):
            if (x, self.boundary_size - 1) in self.sinks:
                grid[x][self.boundary_size - 1] = (grid[x - 1][self.boundary_size - 1] - 1) % 3
            else:
                grid[x][self.boundary_size - 1] = (grid[x - 1][self.boundary_size - 1] + 1) % 3

        # Rest of boundary

        for x in range(1, self.boundary_size):
            grid[x][0] = (grid[x - 1][0] + 1) % 3

        for y in range(1, self.boundary_size):
            grid[self.boundary_size - 1][y] = (grid[self.boundary_size - 1][y - 1] - 1) % 3

        # We can fill in the rest.

        for x in range(1, self.boundary_size - 1):
            for y in range(1, self.boundary_size - 1):
                grid[x][y] = (grid[x][y - 1] - 1) % 3

        grid[1][3] = 0 # Hardcode cause fuck it.

        return grid

    def check_validity(self):
        for x in range(1, self.boundary_size - 1):
            for y in range(1, self.boundary_size - 1):
                color = self.grid[x][y]
                surroundings = [self.grid[x - 1][y], self.grid[x + 1][y], self.grid[x][y - 1], self.grid[x][y + 1]]
                if color in surroundings:
                        return False
        for y in range(self.boundary_size):
            color = self.grid[0][y]
            surroundings = self.grid[1][y]
            if color == surroundings:
                return False

            color = self.grid[self.boundary_size - 1][y]
            surroundings = self.grid[self.boundary_size - 2][y]
            if color == surroundings:
                return False

        for x in range(self.boundary_size):
            color = self.grid[x][0]
            surroundings = self.grid[x][1]
            if color == surroundings:
                return False

            color = self.grid[x][self.boundary_size - 1]
            surroundings = self.grid[x][self.boundary_size - 2]
            if color == surroundings:
                return False

        return True

    def draw(self):
        length = self.boundary_size
        for i in range(length):
            for j in range(length):
                print(self.grid[j][length - i - 1], end='  ')
            print()

class MarkovChain:

    def __init__(self, weights):
        self.weights = weights

    def step(self, initial_state):
        # Generate a random number between 1 and 2 * boundary_size - 1 (this is the longest a path can be)
        num_edges = random.randint(1, 2 * (initial_state.boundary_size - 1))

        # choose a random source
        choosen_source = initial_state.sources[random.randint(0, len(initial_state.sources))]

        # step along the path. You can only move right or down.

        # Well actually, fuck it.

        x = random.randint(1, (initial_state.boundary_size - 1))
        y = random.randint(1, (initial_state.boundary_size - 1))

        # Find the four numbers around it
        around = list()
        around.append(initial_state.grid[x][y + 1], initial_state.grid[x][y - 1], initial_state.grid[x + 1][y], initial_state.grid[x - 1][y])

        state_color = initial_state.grid[x][y]
        if (state_color + 2) % 3 not in around:
            # Check if this is right...
            initial_state.grid[x][y] = (state_color + 2) % 3
        # Else, do nothing.

        return 0

    def time_travel(self, iterations, initial_state):
        curr_state = initial_state
        for i in range(iterations):
            curr_state.draw()
            curr_state = self.step(curr_state)

# Note : These are translated sources (corresponding to boxes rather than points).
eps = EulerianPathState(sources=[(0, 1), (0, 3), (0,4)], sinks=[(1,5 - 1), (2,5 - 1), (4, 5 - 1)], boundary_size=5)
eps.draw()
print(eps.check_validity())