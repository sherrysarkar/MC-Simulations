import numpy as np

class SimpleMarkovChain:
    def __init__(self, list_states, transition_matrix):
        self.states = list_states
        self.num_states = len(self.states)
        self.indexed_states = dict()

        for i in range(self.num_states):
            self.indexed_states[self.states[i]] = i

        self.transition_matrix = transition_matrix

    def step(self, initial_state):
        index_of_curr = self.indexed_states[initial_state]
        prob_row = self.transition_matrix[index_of_curr]

        index_next_state = np.random.choice(len(self.states), 1, prob_row)
        return self.states[index_next_state[0]]

    def time_travel(self, iterations, initial_state):
        curr_state = initial_state
        for i in range(iterations):
            print(curr_state)
            curr_state = self.step(curr_state)

mc = SimpleMarkovChain(list_states=['N', 'S'], transition_matrix=[[0.5, 0.5], [0,5, 0.5]])
mc.time_travel(5, 'N')