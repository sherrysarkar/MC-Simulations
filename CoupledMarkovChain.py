import numpy as np
from matplotlib.path import Path
from matplotlib.patches import PathPatch
import matplotlib.pyplot as plt
import copy

import random


class EulerianPathState:
    def __init__(self, sources, sinks, boundary_size, pinkgrid=[], bluegrid=[]):
        if len(sources) != len(sinks):
            raise Exception("Unequal number of sources and sinks.")
        self.sources = sources
        self.sinks = sinks
        self.boundary_size = boundary_size

        # Let each face be uniquely represented by it's lowest left most corner.
        self.pink_grid = []
        self.blue_grid = []
        if len(pinkgrid) == 0:
            self.generate_paths()
        else:
            self.pink_grid = pinkgrid
            self.blue_grid = bluegrid

    def generate_paths(self):
        self.pink_grid = [[0 for j in range(self.boundary_size)] for i in range(self.boundary_size)]
        self.blue_grid = [[0 for j in range(self.boundary_size)] for i in range(self.boundary_size)]

        # What are our two horizontal lines? y = 3 and y = 5 (hard code for now)

        # Do the bottom row first.
        for x in range(1, self.boundary_size):
            self.blue_grid[x][0] = (self.blue_grid[x - 1][0] + 1) % 3

        for x in range(self.boundary_size):
            for y in range(1, self.boundary_size):
                if x <= 28:
                    if y == 1:
                        self.blue_grid[x][y] = (self.blue_grid[x][y - 1] + 1) % 3
                    else:
                        self.blue_grid[x][y] = (self.blue_grid[x][y - 1] - 1) % 3
                else:
                    self.blue_grid[x][y] = (self.blue_grid[x][y - 1] - 1) % 3

        # Next, the pink stuff.
        for x in range(1, self.boundary_size):
            self.pink_grid[x][0] = (self.pink_grid[x - 1][0] + 1) % 3

        for x in range(self.boundary_size):
            for y in range(1, self.boundary_size):
                if x == 0:
                    if y == 1:
                        self.pink_grid[x][y] = (self.pink_grid[x][y - 1] + 1) % 3
                    else:
                        self.pink_grid[x][y] = (self.pink_grid[x][y - 1] - 1) % 3
                else:
                    if y == 29:
                        self.pink_grid[x][y] = (self.pink_grid[x][y - 1] + 1) % 3
                    else:
                        self.pink_grid[x][y] = (self.pink_grid[x][y - 1] - 1) % 3
                    if x == 29 and y == 29:
                        self.pink_grid[x][y] = (self.pink_grid[x - 1][y] - 1) % 3
    def check_validity(self):
        for x in range(1, self.boundary_size - 1):
            for y in range(1, self.boundary_size - 1):
                color = self.pink_grid[x][y]
                surroundings = [self.pink_grid[x - 1][y], self.pink_grid[x + 1][y], self.pink_grid[x][y - 1], self.pink_grid[x][y + 1]]
                if color in surroundings:
                    return False

        for y in range(1, self.boundary_size):
            color = self.pink_grid[0][y]
            surroundings = [self.pink_grid[1][y], self.pink_grid[0][y - 1]]
            if color in surroundings:
                return False

            color = self.pink_grid[self.boundary_size - 1][y]
            surroundings = [self.pink_grid[self.boundary_size - 2][y], self.pink_grid[self.boundary_size - 1][y - 1]]
            if color in surroundings:
                return False

        for x in range(1, self.boundary_size):
            color = self.pink_grid[x][0]
            surroundings = [self.pink_grid[x][1], self.pink_grid[x - 1][0]]
            if color in surroundings:
                return False

            color = self.pink_grid[x][self.boundary_size - 1]
            surroundings = [self.pink_grid[x][self.boundary_size - 2], self.pink_grid[x - 1][self.boundary_size - 1]]
            if color in surroundings:
                return False

        return True

    def draw(self):
        length = self.boundary_size
        for i in range(length):
            for j in range(length):
                print(self.pink_grid[j][length - i - 1], end='  ')
            print()
        #print(self.Rs, self.Us)
        print()

    def set_up_GUI(self):
        pink_vertices = []
        pink_codes = []
        # First, write in horizontal edges
        for x in range(self.boundary_size - 1):  # Are all these -1's right? Somehow, I doubt it...
            for y in range(self.boundary_size - 1):
                if (self.pink_grid[x][y] + 1) % 3 == self.pink_grid[x][y + 1]:
                    pink_vertices += [(x, y + 1), (x + 1, y + 1)]
                    pink_codes += [Path.MOVETO]
                    pink_codes += [Path.LINETO]

        for y in range(self.boundary_size):
            for x in range(self.boundary_size - 1):
                if (self.pink_grid[x][y] - 1) % 3 == self.pink_grid[x + 1][y]:
                    pink_vertices += [(x + 1, y + 1), (x + 1, y)]
                    pink_codes += [Path.MOVETO]
                    pink_codes += [Path.LINETO]

        blue_vertices = []
        blue_codes = []
        # First, write in horizontal edges
        for x in range(self.boundary_size - 1):  # Are all these -1's right? Somehow, I doubt it...
            for y in range(self.boundary_size - 1):
                if (self.blue_grid[x][y] + 1) % 3 == self.blue_grid[x][y + 1]:
                    blue_vertices += [(x, y + 1), (x + 1, y + 1)]
                    blue_codes += [Path.MOVETO]
                    blue_codes += [Path.LINETO]

        for y in range(self.boundary_size):
            for x in range(self.boundary_size - 1):
                if (self.blue_grid[x][y] - 1) % 3 == self.blue_grid[x + 1][y]:
                    blue_vertices += [(x + 1, y + 1), (x + 1, y)]
                    blue_codes += [Path.MOVETO]
                    blue_codes += [Path.LINETO]

        return pink_vertices, pink_codes, blue_vertices, blue_codes

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

        pink_vertices, pink_codes, blue_vertices, blue_codes = self.set_up_GUI()  # IMPORTANT LINE OF CODE.

        ############

        blue_vertices = np.array(blue_vertices, float)
        blue_path = Path(blue_vertices, blue_codes)

        blue_patch = PathPatch(blue_path, facecolor='None', edgecolor='blue', linewidth=2.0)
        ax.add_patch(blue_patch)

        ############

        pink_vertices = np.array(pink_vertices, float)
        path = Path(pink_vertices, pink_codes)

        pathpatch = PathPatch(path, facecolor='None', edgecolor='pink', linewidth=2.0)
        ax.add_patch(pathpatch)

        #############

        ax.set_title('Eularian Routings on Bounded Lattice: Iteration ' + str(i))
        ax.dataLim.update_from_data_xy(pink_vertices)
        ax.set_xlim(0, self.boundary_size)
        ax.set_ylim(0, self.boundary_size)

        plt.show()

class MarkovChain:

    def __init__(self, weights=[1, 1, 1, 1, 1, 1]):
        self.weights = [(w / np.sum(weights)) for w in weights]
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
            return 100

        if (config[3]) % 3 == 2: # CAUTION
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

    def find_config_of_vertex(self, vertex, state, pink):
        if vertex[0] == 30 or vertex[1] == 30:
            return False

        config = list()
        config.append(0)

        if pink:
            config.append(state.pink_grid[vertex[0] - 1][vertex[1]] - state.pink_grid[vertex[0]][vertex[1]])  # error is [0, 2, 0, 1]
            config.append(state.pink_grid[vertex[0] - 1][vertex[1] - 1] - state.pink_grid[vertex[0]][vertex[1]])
            config.append(state.pink_grid[vertex[0]][vertex[1] - 1] - state.pink_grid[vertex[0]][vertex[1]])
        else:
            config.append(state.blue_grid[vertex[0] - 1][vertex[1]] - state.blue_grid[vertex[0]][vertex[1]])  # error is [0, 2, 0, 1]
            config.append(state.blue_grid[vertex[0] - 1][vertex[1] - 1] - state.blue_grid[vertex[0]][vertex[1]])
            config.append(state.blue_grid[vertex[0]][vertex[1] - 1] - state.blue_grid[vertex[0]][vertex[1]])

        return config

    def score(self, old_state, new_state, vertex_of_change, pink):
        # We take the entire square, so 9 vertices to consider.
        new_score = 1
        x,y = vertex_of_change

        for dx in range(-1, 1):
            for dy in range(-1, 1):
                new_score = new_score * self.weights[self.function(self.find_config_of_vertex(vertex=(x + dx, y + dy), state=new_state, pink=pink))]

        old_score = 1
        x, y = vertex_of_change

        for dx in range(-1, 1):
            for dy in range(-1, 1):
                old_score = old_score * self.weights[self.function(self.find_config_of_vertex(vertex=(x + dx, y + dy), state=old_state, pink=pink))]

        ratio = new_score / old_score

        return min(ratio, 1)

    def flip(self, initial_state, vertex, valley, pink):
        #print("Got to Flip")
        state = EulerianPathState(copy.deepcopy(initial_state.sources), copy.deepcopy(initial_state.sinks), initial_state.boundary_size, copy.deepcopy(initial_state.pink_grid), copy.deepcopy(initial_state.blue_grid))

        if pink:
            if valley:
                if self.function(self.find_config_of_vertex(vertex, state, pink)) <= 1:
                    state.pink_grid[vertex[0] - 1][vertex[1]] = (state.pink_grid[vertex[0] - 1][vertex[1]] + 1) % 3
                    if state.check_validity() is False:
                        print("Beginning of Error")
                        initial_state.draw()
                        state.draw()
                        state.draw_GUI("Error")
                        print(vertex)
                        raise "Incorrect state made at Flip, Valley"
                    return state
            else:
                if self.function(self.find_config_of_vertex(vertex, state, pink)) == 0 or 2:
                    state.pink_grid[vertex[0]][vertex[1] - 1] = (state.pink_grid[vertex[0]][vertex[1] - 1] - 1) % 3
                    if state.check_validity() is False:
                        print("Beginning of Error")
                        initial_state.draw()
                        state.draw()
                        state.draw_GUI("Error")
                        print(vertex)
                        raise "Incorrect state made at Flip, Peak"
                    return state
        else:
            if valley:
                if self.function(self.find_config_of_vertex(vertex, state, pink)) <= 1:
                    state.blue_grid[vertex[0] - 1][vertex[1]] = (state.blue_grid[vertex[0] - 1][vertex[1]] + 1) % 3
                    if state.check_validity() is False:
                        print("Beginning of Error")
                        initial_state.draw()
                        state.draw()
                        state.draw_GUI("Error")
                        print(vertex)
                        raise "Incorrect state made at Flip, Valley"
                    return state
            else:
                if self.function(self.find_config_of_vertex(vertex, state, pink)) == 0 or 2:
                    state.blue_grid[vertex[0]][vertex[1] - 1] = (state.blue_grid[vertex[0]][vertex[1] - 1] - 1) % 3
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
        pink_vertices, pink_codes, blue_vertices, blue_codes = initial_state.set_up_GUI()

        p = random.randint(0, (len(pink_vertices) - 1))

        pink_vertex = (1,29) #pink_vertices[p]
        blue_vertex = blue_vertices[p]
        change = False
        next_state = EulerianPathState(copy.deepcopy(initial_state.sources), copy.deepcopy(initial_state.sinks), initial_state.boundary_size, copy.deepcopy(initial_state.pink_grid), copy.deepcopy(initial_state.blue_grid))

        while 30 in pink_vertex or 0 in pink_vertex or 30 in blue_vertex or 0 in blue_vertex:
            p = random.randint(0, (len(pink_vertices) - 1))
            pink_vertex = pink_vertices[p]
            blue_vertex = blue_vertices[p]#print("uhoh...")

        r = random.random()

        ### Do things with pink vertex // valley valley peak peak

        if r < 0.5:
            # If vertex is valley
            if self.function(self.find_config_of_vertex(pink_vertex, initial_state, True)) <= 1:
                # and the bottom of a tower of height 1, then
                if self.function(self.find_config_of_vertex((pink_vertex[0] - 1, pink_vertex[1] + 1), initial_state, True)) == 5:
                    R_2 = self.flip(initial_state, pink_vertex, True, True)
                    pi = self.score(initial_state, R_2, pink_vertex, True)
                    if r <= 0.5 * pi:
                        next_state = R_2
                        change = True

            ### Do things with blue vertex

            if self.function(self.find_config_of_vertex(blue_vertex, next_state, False)) <= 1:
                # and the bottom of a tower of height 1, then
                if self.function(self.find_config_of_vertex((blue_vertex[0] - 1, blue_vertex[1] + 1), next_state, False)) == 5:
                    R_2 = self.flip(next_state, blue_vertex, True, False)
                    pi = self.score(next_state, R_2, blue_vertex, False)
                    if r <= 0.5 * pi:
                        next_state = R_2
                        change = True
        else:
            print("peak position")
            print(self.find_config_of_vertex(pink_vertex, initial_state, True))
            print(self.function(self.find_config_of_vertex(pink_vertex, initial_state, True)))
            print("done")
            if self.function(self.find_config_of_vertex(pink_vertex, initial_state, True)) == 0 or self.function(self.find_config_of_vertex(pink_vertex, initial_state, True)) == 2:
                #print("is Peak")
                if self.function(self.find_config_of_vertex((pink_vertex[0] + 1, pink_vertex[1] - 1), initial_state, True)) == 5:
                    R_2 = self.flip(initial_state, pink_vertex, False, True)
                    pi = self.score(initial_state, R_2, pink_vertex, True)
                    if r >= 1 - pi * 0.5:
                        next_state = R_2
                        change = True
            ### Blue
            if self.function(self.find_config_of_vertex(blue_vertex, next_state, False)) == 0 or self.function(self.find_config_of_vertex(blue_vertex, next_state, False)) == 2:
                if self.function(self.find_config_of_vertex((blue_vertex[0] + 1, blue_vertex[1] - 1), next_state, False)) == 5:
                    R_2 = self.flip(next_state, blue_vertex, False, False)
                    pi = self.score(next_state, R_2, blue_vertex, False)
                    if r >= 1 - pi * 0.5:
                        next_state = R_2
                        change = True

        return next_state, change

    def time_travel(self, iterations, initial_state):
        curr_state = initial_state
        curr_state.draw_GUI("Initial State")
        for i in range(iterations):
            print("Start Iteration " + str(i))
            curr_state, boolean = self.step(curr_state)
            #curr_state.draw()
            if boolean:
                curr_state.draw_GUI(i)


# Note : These are translated sources (corresponding to boxes rather than points).
eps = EulerianPathState(sources=[(0, 1)], sinks=[(29,30 - 1)], boundary_size=30)  # only works with 5
#eps.draw()
#eps.draw_GUI("Trail")
mc = MarkovChain(weights=[1, 1, 1, 1, 1, 1])
mc.time_travel(1000, eps)

