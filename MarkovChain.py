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
        self.grid = []
        if len(grid) == 0:
            self.generate_paths()
        else:
            self.grid = grid

    def small_generate_paths(self):
        # generate a valid Eulerian Routing
        self.grid = [[0 for j in range(self.boundary_size)] for i in range(self.boundary_size)]

        # First, go around the boundary, with sources then sinks.
        for y in range(1, self.boundary_size):
            if (0, y) in self.sources:
                self.grid[0][y] = (self.grid[0][y - 1] + 1) % 3
            else:
                self.grid[0][y] = (self.grid[0][y - 1] - 1) % 3

        for x in range(1, self.boundary_size):
            if (x, self.boundary_size - 1) in self.sinks:
                self.grid[x][self.boundary_size - 1] = (self.grid[x - 1][self.boundary_size - 1] - 1) % 3
            else:
                self.grid[x][self.boundary_size - 1] = (self.grid[x - 1][self.boundary_size - 1] + 1) % 3

        # Rest of boundary

        for x in range(1, self.boundary_size):
            self.grid[x][0] = (self.grid[x - 1][0] + 1) % 3

        for y in range(1, self.boundary_size):
            self.grid[self.boundary_size - 1][y] = (self.grid[self.boundary_size - 1][y - 1] - 1) % 3

        # We can fill in the rest.
        self.draw()

        while self.check_validity() is not True:
            print("Here!")
            for x in range(1, self.boundary_size - 1):
                for y in range(1, self.boundary_size - 1):
                    self.grid[x][y] = random.randint(0,2)
                    self.draw()

        # for x in range(1, self.boundary_size - 1):
        #     for y in range(1, self.boundary_size - 1):
        #         grid[x][y] = (grid[x][y - 1] - 1) % 3
        #
        # grid[1][3] = 0 # Hardcode cause fuck it. // Usual Method

    def generate_paths(self):
        self.grid = [[0 for j in range(self.boundary_size)] for i in range(self.boundary_size)]

        # What are our two horizontal lines? y = 3 and y = 5 (hard code for now)

        # Do the base line first.
        for x in range(1, self.boundary_size):
            self.grid[x][0] = (self.grid[x - 1][0] + 1) % 3

        for x in range(self.boundary_size):
            for y in range(1, self.boundary_size):
                if x <= 24:
                    if y == 3 or y == 5:
                        self.grid[x][y] = (self.grid[x][y - 1] + 1) % 3
                    else:
                        self.grid[x][y] = (self.grid[x][y - 1] - 1) % 3
                elif x <= 26:
                    if y== 3:
                        self.grid[x][y] = (self.grid[x][y - 1] + 1) % 3
                    else:
                        self.grid[x][y] = (self.grid[x][y - 1] - 1) % 3
                else:
                    self.grid[x][y] = (self.grid[x][y - 1] - 1) % 3

    def count_edges(self):
        vertices = []

        for x in range(self.boundary_size - 1):  # Are all these -1's right? Somehow, I doubt it...
            for y in range(self.boundary_size - 1):
                if (self.grid[x][y] + 1) % 3 == self.grid[x][y + 1]:
                    vertices += [(x, y + 1), (x + 1, y + 1)]

        if len(vertices) % 2 == 0:
            rights = len(vertices) / 2
        else:
            raise "Number of vertices for rights was odd."

        for y in range(self.boundary_size):
            for x in range(self.boundary_size - 1):
                if (self.grid[x][y] - 1) % 3 == self.grid[x + 1][y]:
                    vertices += [(x + 1, y + 1), (x + 1, y)]

        if len(vertices) % 2 == 0:
            ups = (len(vertices) / 2) - rights
        else:
            raise "Number of vertices for rights was odd."

        return rights, ups

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
        #print(self.Rs, self.Us)
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

        print(len(vertices))
        return vertices, codes

    def draw_GUI(self, i):

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
        ax.set_title('Eularian Routings on Bounded Lattice: Iteration ' + str(i))

        ax.dataLim.update_from_data_xy(vertices)
        ax.set_xlim(0, self.boundary_size)
        ax.set_ylim(0, self.boundary_size)

        plt.show()

class MarkovChain:

    def __init__(self, weights=[1, 1, 1, 1, 1, 1]):
        self.weights = [(w / np.sum(weights)) for w in weights]
        self.weights += [1]
        self.configurations = []

        # Going in a counter clockwise direction through the four boxes
        self.configurations.append([0, 1, 0, -1])  # CROSS                  0
        self.configurations.append([0, 1, 0, 1])  # VALLEY                  1
        self.configurations.append([0, -1, 0, -1])  # PEAK                  2
        self.configurations.append([0, 1, -1, 1])  # VERTICAL LINE          3
        self.configurations.append([0, -1, 1, -1])  # HORIZONTAL LINE       4
        self.configurations.append([0, -1, 0, 1])  # EMPTY                  5

    def function(self, config):
        if not config:
            return 6

        if (config[3]) % 3 == 2:
            if (config[2] + config[1]) % 3 == 2:
                return 2
            elif (config[2] + config[1]) % 3 == 0:
                return 4
            else:
                return 0
        else:
            if (config[2] + config[1]) % 3 == 2:
                return 5
            elif (config[2] + config[1]) % 3 == 0:
                return 3
            else:
                return 1

    def find_config_of_vertex(self, vertex, state):
        if vertex[0] >= state.boundary_size or vertex[1] >= state.boundary_size:
            return False

        config = list()
        config.append(0)
        config.append(state.grid[vertex[0] - 1][vertex[1]] - state.grid[vertex[0]][vertex[1]]) # error is [0, 2, 0, 1]
        config.append(state.grid[vertex[0] - 1][vertex[1] - 1] - state.grid[vertex[0]][vertex[1]])
        config.append(state.grid[vertex[0]][vertex[1] - 1] - state.grid[vertex[0]][vertex[1]])
        return config

    def score(self, old_state, new_state, vertex_of_change):
        # We take the entire square, so 9 vertices to consider.
        new_score = 1
        x, y = vertex_of_change

        for dx in range(-1, 2):
            for dy in range(-1, 2):
                new_score = new_score * self.weights[
                    self.function(self.find_config_of_vertex(vertex=(x + dx, y + dy), state=new_state))]

        old_score = 1
        x, y = vertex_of_change

        for dx in range(-1, 2):
            for dy in range(-1, 2):
                old_score = old_score * self.weights[
                    self.function(self.find_config_of_vertex(vertex=(x + dx, y + dy), state=old_state))]

        ratio = new_score / old_score

        return min(ratio, 1)

    def flip(self, initial_state, vertex, valley):
        #print("Got to Flip")
        state = EulerianPathState(copy.deepcopy(initial_state.sources), copy.deepcopy(initial_state.sinks), initial_state.boundary_size, copy.deepcopy(initial_state.grid))

        if valley:
            if self.function(self.find_config_of_vertex(vertex, state)) <= 1:
                state.grid[vertex[0] - 1][vertex[1]] = (state.grid[vertex[0] - 1][vertex[1]] + 1) % 3
                if state.check_validity() is False:
                    print("Beginning of Error")
                    initial_state.draw()
                    state.draw()
                    state.draw_GUI("Error")
                    print(vertex)
                    raise "Incorrect state made at Flip, Valley"
                return state
        else:
            if self.function(self.find_config_of_vertex(vertex, state)) == 0 or 2:
                state.grid[vertex[0]][vertex[1] - 1] = (state.grid[vertex[0]][vertex[1] - 1] - 1) % 3
                if state.check_validity() is False:
                    print("Beginning of Error")
                    initial_state.draw()
                    state.draw()
                    state.draw_GUI("Error")
                    print(vertex)
                    raise "Incorrect state made at Flip, Peak"
                return state

        raise "This is not a peak or valley."


    def step(self, initial_state):
        vertices, codes = initial_state.set_up_GUI()

        #print(vertices)

        vertex = vertices[random.randint(0, (len(vertices) - 1))]
        while 30 in vertex or 0 in vertex:
            vertex = vertices[random.randint(0, (len(vertices) - 1))]
            #print("uhoh...")
        r = random.random()

        if r < 0.5:
            # If vertex is valley
            if self.function(self.find_config_of_vertex(vertex, initial_state)) <= 1:
                # and the bottom of a tower of height 1, then
                #print("is Valley")
                if self.function(self.find_config_of_vertex((vertex[0] - 1, vertex[1] + 1), initial_state)) == 5:
                    R_2 = self.flip(initial_state, vertex, True)
                    pi = self.score(initial_state, R_2, vertex)
                    if r <= 0.5 * pi:
                        return R_2, True
        else:
            if self.function(self.find_config_of_vertex(vertex, initial_state)) == 0 or self.function(self.find_config_of_vertex(vertex, initial_state)) == 2:
                #print("is Peak")
                if self.function(self.find_config_of_vertex((vertex[0] + 1, vertex[1] - 1), initial_state)) == 5:
                    R_2 = self.flip(initial_state, vertex, False)
                    pi = self.score(initial_state, R_2, vertex)
                    if r >= 1 - pi * 0.5:
                        return R_2, True

        #print("Never did anything")
        return initial_state, False

    def time_travel(self, iterations, initial_state):
        curr_state = initial_state
        curr_state.draw_GUI("Initial State")
        for i in range(iterations):
            print("Start Iteration " + str(i))
            curr_state, boolean = self.step(curr_state)
            if boolean:
                if i >= 4950:
                    curr_state.draw_GUI(i)


# Note : These are translated sources (corresponding to boxes rather than points).
eps = EulerianPathState(sources=[(0, 3), (0, 5)], sinks=[(26,30 - 1), (24,30 - 1)], boundary_size=30)  # only works with 5
#eps.draw()
#eps.draw_GUI()
mc = MarkovChain(weights=[2, 1, 1, 2, 2, 2])
mc.time_travel(5000, eps)

