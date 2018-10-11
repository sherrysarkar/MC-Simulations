import numpy as np
import copy
from SixVMState import SixVMState
import random

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
        state = SixVMState(copy.deepcopy(initial_state.sources), copy.deepcopy(initial_state.sinks), initial_state.boundary_size, copy.deepcopy(initial_state.grid), copy.deepcopy(initial_state.vertices))

        if valley:
            if self.function(self.find_config_of_vertex(vertex, state)) <= 1:
                state.grid[vertex[0] - 1][vertex[1]] = (state.grid[vertex[0] - 1][vertex[1]] + 1) % 3
                if state.check_validity() is False:
                    print("Beginning of Error")
                    initial_state.draw()
                    state.draw()
                    state.draw_GUI("Error")
                    #print(vertex)
                    raise "Incorrect state made at Flip, Valley"
                return state
        else:
            if self.function(self.find_config_of_vertex(vertex, state)) == 0 or self.function(self.find_config_of_vertex(vertex, state)) == 2:
                state.grid[vertex[0]][vertex[1] - 1] = (state.grid[vertex[0]][vertex[1] - 1] - 1) % 3
                if state.check_validity() is False:
                    print("Beginning of Error")
                    initial_state.draw()
                    state.draw()
                    state.draw_GUI("Error")
                    #print(vertex)
                    raise "Incorrect state made at Flip, Peak"
                return state

        raise "This is not a peak or valley."

    def step(self, initial_state):  # Should be EPS state.
        vertices = initial_state.vertices  # TODO: This line is extremely inefficient.

        vertex = vertices[random.randint(0, (len(vertices) - 1))]
        while initial_state.boundary_size - 1 in vertex or 0 in vertex:
            vertex = vertices[random.randint(0, (len(vertices) - 1))]
        r = random.random()

        if r < 0.5:
            # If vertex is valley
            if self.function(self.find_config_of_vertex(vertex, initial_state)) <= 1:
                # and the bottom of a tower of height 1, then
                if self.function(self.find_config_of_vertex((vertex[0] - 1, vertex[1] + 1), initial_state)) == 5:
                    R_2 = self.flip(initial_state, vertex, True)
                    pi = self.score(initial_state, R_2, vertex)
                    if r <= 0.5 * pi:
                        R_2.vertices.remove(vertex)
                        R_2.vertices.append((vertex[0] - 1, vertex[1] + 1))
                        return R_2, True
        else:
            if self.function(self.find_config_of_vertex(vertex, initial_state)) == 0 or self.function(self.find_config_of_vertex(vertex, initial_state)) == 2:
                if self.function(self.find_config_of_vertex((vertex[0] + 1, vertex[1] - 1), initial_state)) == 5:
                    R_2 = self.flip(initial_state, vertex, False)
                    pi = self.score(initial_state, R_2, vertex)
                    if r >= 1 - pi * 0.5:
                        R_2.vertices.remove(vertex)
                        R_2.vertices.append((vertex[0] + 1, vertex[1] - 1))
                        return R_2, True

        return initial_state, False

    def time_travel(self, iterations, initial_state):
        curr_state = initial_state
        curr_state.draw_GUI("Initial State")
        for i in range(iterations):
            print("Start Iteration " + str(i))
            curr_state, boolean = self.step(curr_state)
            if boolean:
                if i >= iterations - 1000 and i <= iterations:
                    curr_state.draw_GUI(i)

# Note : These are translated sources (corresponding to boxes rather than points).
def determine_sources_sinks():
    sources = []
    sinks = []
    for i in range(1, 10):
        sources.append((0, i))
        sinks.append((100, 100 - i))
    return sources, sinks

sources, sinks = determine_sources_sinks()
eps = SixVMState(sources=sources, sinks=sinks, boundary_size=100)
#eps.draw()
#eps.draw_GUI(0)
mc = MarkovChain()
mc.time_travel(200000, eps)

