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

    def __init__(self, weights=[1, 1, 1, 1, 1, 1]):
        self.weights = [(w / np.sum(weights)) for w in weights]
        self.configurations = []

        # Going in a counter clockwise direction through the four boxes
        self.configurations.append([0, 1, 0, -1])  # CROSS
        self.configurations.append([0, 1, 0, 1])  # BACKWARDS L
        self.configurations.append([0, -1, 0, -1])  # CORNER
        self.configurations.append([0, 1, -1, 1])  # VERTICAL LINE
        self.configurations.append([0, -1, 1, -1])  # HORIZONTAL LINE
        self.configurations.append([0, -1, 0, 1])  # EMPTY

    def replace_four(self, initial_state, vertex, config):
        state = EulerianPathState(initial_state.sources, initial_state.sinks, initial_state.boundary_size, initial_state.grid)

        state.grid[vertex[0] - 1][vertex[1]] = state.grid[vertex[0] - 1][vertex[1]] + config[1]
        state.grid[vertex[0] - 1][vertex[1] - 1] = state.grid[vertex[0] - 1][vertex[1] - 1] + config[2]
        state.grid[vertex[0]][vertex[1] - 1] = state.grid[vertex[0]][vertex[1] - 1] + config[3]

        return state

    def score(self, old_state, new_state, vertex_of_change):
        return random.randint(0, 5)

    def step(self, initial_state):
        x = random.randint(1, (initial_state.boundary_size - 1))
        y = random.randint(1, (initial_state.boundary_size - 1))

        vertex = (3,3)
        valid_colorings = []

        for config in self.configurations:
            state = self.replace_four(initial_state, vertex, config)
            if state.check_validity():
                valid_colorings.append(state)

        scores = []

        for valid in valid_colorings:
            scores.append(self.score(initial_state, valid, vertex))

        for x in valid_colorings:
            x.draw()
            print()

        return valid_colorings[1]

    def time_travel(self, iterations, initial_state):
        curr_state = initial_state
        for i in range(iterations):
            #curr_state.draw()
            #print(curr_state.check_validity())
            #print("done")
            curr_state = self.step(curr_state)

# Note : These are translated sources (corresponding to boxes rather than points).
eps = EulerianPathState(sources=[(0, 1), (0, 3), (0,4)], sinks=[(1,5 - 1), (2,5 - 1), (4, 5 - 1)], boundary_size=5)
#eps.draw()
#print(eps.check_validity())
mc = MarkovChain()
mc.time_travel(1, eps)