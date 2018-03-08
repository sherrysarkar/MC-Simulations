import numpy as np
from matplotlib.path import Path
from matplotlib.patches import PathPatch
import matplotlib.pyplot as plt
import copy

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

        for y in range(1, self.boundary_size):
            color = self.grid[0][y]
            surroundings = [self.grid[1][y], self.grid[0][y - 1]]
            if color in surroundings:
                return False

            color = self.grid[self.boundary_size - 1][y]
            surroundings = [self.grid[self.boundary_size - 2][y], self.grid[self.boundary_size - 1][y - 1]]
            if color in surroundings:
                return False

        for x in range(1, self.boundary_size):
            color = self.grid[x][0]
            surroundings = [self.grid[x][1], self.grid[x - 1][0]]
            if color in surroundings:
                return False

            color = self.grid[x][self.boundary_size - 1]
            surroundings = [self.grid[x][self.boundary_size - 2], self.grid[x - 1][self.boundary_size - 1]]
            if color in surroundings:
                return False

        return True

    def draw(self):
        length = self.boundary_size
        for i in range(length):
            for j in range(length):
                print(self.grid[j][length - i - 1], end='  ')
            print()
        print()

    def set_up_GUI(self):
        vertices = []
        codes = []
        # First, write in horizontal edges
        for x in range(self.boundary_size - 1):  # Are all these -1's right? Somehow, I doubt it...
            for y in range(self.boundary_size - 1):
                if (self.grid[x][y] + 1) % 3 == self.grid[x][y + 1]:
                    vertices += [(x, y + 1), (x + 1, y + 1)]
                    codes += [Path.MOVETO]
                    codes += [Path.LINETO]

        for y in range(self.boundary_size):
            for x in range(self.boundary_size - 1):
                if (self.grid[x][y] - 1) % 3 == self.grid[x + 1][y]:
                    vertices += [(x + 1, y + 1), (x + 1, y)]
                    codes += [Path.MOVETO]
                    codes += [Path.LINETO]

        return vertices, codes

    def draw_GUI(self):

        fig, ax = plt.subplots()

        lattice_vertices = []
        lattice_code = []

        for y in range(self.boundary_size + 2):
            lattice_vertices += [(0, y), (self.boundary_size + 2, y)]
        lattice_code += [Path.MOVETO, Path.LINETO] * (self.boundary_size + 2)

        for x in range(self.boundary_size + 2):
            lattice_vertices += [(x, 0), (x, self.boundary_size + 2)]
        lattice_code += [Path.MOVETO, Path.LINETO] * (self.boundary_size + 2)

        lattice_vertices = np.array(lattice_vertices, float)
        lattice = Path(lattice_vertices, lattice_code)

        lattice_path = PathPatch(lattice, facecolor='None', edgecolor='grey', linestyle='dotted')
        ax.add_patch(lattice_path)

        vertices, codes = self.set_up_GUI()  # IMPORTANT LINE OF CODE.

        vertices = np.array(vertices, float)
        path = Path(vertices, codes)

        pathpatch = PathPatch(path, facecolor='None', edgecolor='green', linewidth=2.0)

        ax.add_patch(pathpatch)
        ax.set_title('Eularian Routings on Bounded Lattice')

        ax.dataLim.update_from_data_xy(vertices)
        ax.set_xlim(0, self.boundary_size)
        ax.set_ylim(0, self.boundary_size)

        plt.show()

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
        state = EulerianPathState(copy.deepcopy(initial_state.sources), copy.deepcopy(initial_state.sinks), initial_state.boundary_size, copy.deepcopy(initial_state.grid))

        x = state.grid[vertex[0]][vertex[1]]
        state.grid[vertex[0] - 1][vertex[1]] = (x + config[1]) % 3
        state.grid[vertex[0] - 1][vertex[1] - 1] = (x + config[2]) % 3
        state.grid[vertex[0]][vertex[1] - 1] = (x + config[3]) % 3

        if state.check_validity():
            #state.draw()
            return state

        return None

    def score(self, old_state, new_state, vertex_of_change):
        return random.randint(0, 5)

    def step(self, initial_state):
        x = random.randint(1, (initial_state.boundary_size - 1))
        y = random.randint(1, (initial_state.boundary_size - 1))

        vertex = (1,3)
        valid_colorings = []

        for config in self.configurations:
            state = self.replace_four(initial_state, vertex, config)
            if state is not None:
                valid_colorings.append(state)

        r = random.randint(0, len(valid_colorings) - 1)
        return valid_colorings[r]

    def time_travel(self, iterations, initial_state):
        curr_state = initial_state
        for i in range(iterations):
            print("Start Iteration " + str(i))
            curr_state = self.step(curr_state)
            curr_state.draw()

# Note : These are translated sources (corresponding to boxes rather than points).
eps = EulerianPathState(sources=[(0, 1), (0, 3), (0,4)], sinks=[(1,5 - 1), (2,5 - 1), (4, 5 - 1)], boundary_size=5)
#eps.draw()
mc = MarkovChain()
eps.draw()
eps.draw_GUI()