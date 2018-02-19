import numpy as np
from matplotlib.path import Path
from matplotlib.patches import PathPatch
import matplotlib.pyplot as plt


class EulerianPathState:
    def __init__(self, sources, sinks, paths=[]):
        if len(sources) != len(sinks):
            raise Exception("Unequal number of sources and sinks.")
        self.sources = sources
        self.sinks = sinks

        self.max_x = max([sink[0] for sink in self.sinks])
        self.max_y = max([source[1] for source in self.sources])

        self.num_paths = len(self.sources)
        self.paths = paths

        if len(paths) == 0:
            self.generate_paths()

    def generate_paths(self):
        # generate a valid Eulerian Routing

        for i in range(self.num_paths):
            path = list()
            path.append(self.sources[i])

            delta_x = self.sinks[i][0] - self.sources[i][0]

            if delta_x < 0:
                raise Exception("Incorrect source / sink placement. ")

            for d in range(1, delta_x + 1):
                path.append((self.sources[i][0] + d, self.sources[i][1]))  # Is it allowed to go on the boundary?

            delta_y = self.sources[i][1] - self.sinks[i][1]

            if delta_y < 0:
                raise Exception("Incorrect source / sink placement. ")

            for d in range(1, delta_y + 1):
                path.append((self.sources[i][0] + delta_x, self.sources[i][1] - d))

            self.paths.append(path)

    def draw(self):

        fig, ax = plt.subplots()

        lattice_vertices = []
        lattice_code = []

        for y in range(self.max_y + 1):
            lattice_vertices += [(0, y), (self.max_x, y)]
        lattice_code += [Path.MOVETO, Path.LINETO] * (self.max_y + 1)

        for x in range(self.max_x + 1):
            lattice_vertices += [(x, 0), (x, self.max_y)]
        lattice_code += [Path.MOVETO, Path.LINETO] * (self.max_x + 1)

        lattice_vertices = np.array(lattice_vertices, float)
        lattice = Path(lattice_vertices, lattice_code)

        lattice_path = PathPatch(lattice, facecolor='None', edgecolor='grey', linestyle='dotted')
        ax.add_patch(lattice_path)

        vertices = []
        codes = []

        for i in range(len(self.paths)):
            codes += [Path.MOVETO] + [Path.LINETO] * (len(self.paths[i]) - 1)
            vertices += self.paths[i]

        vertices = np.array(vertices, float)
        path = Path(vertices, codes)

        pathpatch = PathPatch(path, facecolor='None', edgecolor='green', linewidth=2.0)

        ax.add_patch(pathpatch)
        ax.set_title('Eularian Routings on Bounded Lattice')

        ax.dataLim.update_from_data_xy(vertices)
        ax.autoscale_view()

        plt.show()

class MarkovChain:

    def step(self, initial_state):
        return 0

    def time_travel(self, iterations, initial_state):
        curr_state = initial_state
        for i in range(iterations):
            curr_state.draw()
            curr_state = self.step(curr_state)

sources, sinks = [(0,7), (0, 6), (0,3)], [(5, 2), (4, 1), (5, 3)]
state = EulerianPathState(sources, sinks)
print(state.paths[0])
state.draw()