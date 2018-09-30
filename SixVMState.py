import numpy as np
from matplotlib.path import Path
from matplotlib.patches import PathPatch
import matplotlib.pyplot as plt

class SixVMState:
    def __init__(self, sources, sinks, boundary_size, grid=[]):
        if len(sources) != len(sinks):
            raise Exception("Unequal number of sources and sinks.")
        self.sources = sources
        self.sinks = sinks
        self.boundary_size = boundary_size  # If boundary size is 5, the x coordinates go up to 4.

        # Let each face be uniquely represented by it's lowest left most corner.
        self.grid = []
        if len(grid) == 0:
            self.generate_unique_minimum()
        else:
            self.grid = grid

    def generate_unique_minimum_edges(self):
        #modified_sources = [(x, -y) for (x, y) in self.sources]  # y turned to -y to help sort.
        #modified_sinks = [(x, -y) for (x, y) in self.sinks]

        sorted_sources = sorted(self.sources)
        sorted_sinks = sorted(self.sinks)

        #modified_sources = [(x, -y) for (x, y) in sorted_sources]  # y turned to -y to help sort.
        #modified_sinks = [(x, -y) for (x, y) in sorted_sinks]

        print(sorted_sources)
        print(sorted_sinks)  # TODO: SORTED NEEDS FIXING.
        print()

        paired_sources_sinks = list(zip(sorted_sources, sorted_sinks))
        boundary = list()
        taken = list()

        for i in range(self.boundary_size):
            sink_y = [y for (x,y) in self.sinks]
            sink_x = [x for (x,y) in self.sinks]
            if i not in sink_y:
                boundary.append(((self.boundary_size - 1, i), (self.boundary_size, i)))
            if i not in sink_x:
                boundary.append(((i, self.boundary_size - 1), (i, self.boundary_size)))

        vertex_taken = [[0 for j in range(self.boundary_size + 1)] for i in range(self.boundary_size + 1)]
        for edge in boundary:
            first = edge[0]
            second = edge[1]
            vertex_taken[first[0]][first[1]] += 1
            vertex_taken[second[0]][second[1]] += 1

        for i in range(len(paired_sources_sinks)):
            print(paired_sources_sinks[i][0])  # TODO: The bug is the fact that both 2 and 3 might be invalid. No wait, nested... shit.
            particle = paired_sources_sinks[i][0]  # Start at the source
            end = paired_sources_sinks[i][1]

            while particle != end:
                if particle[0] < end[0]:  # Horizontal movement case
                    edge = ((particle[0], particle[1]), (particle[0] + 1, particle[1]))
                    n_v = (edge[1][0], edge[1][1])

                    if edge not in taken and edge not in boundary and vertex_taken[n_v[0]][n_v[1]] < 2:
                        vertex_taken[particle[0]][particle[1]] += 1
                        vertex_taken[n_v[0]][n_v[1]] += 1
                        particle = n_v  # Success in taking point.
                        taken.append(edge)

                    elif particle[1] < end[1]:  # Vertical movement case
                        edge = ((particle[0], particle[1]), (particle[0], particle[1] + 1))
                        n_v = (edge[1][0], edge[1][1])
                        if edge not in taken and edge not in boundary and vertex_taken[n_v[0]][n_v[1]] < 2:
                            vertex_taken[particle[0]][particle[1]] += 1
                            vertex_taken[n_v[0]][n_v[1]] += 1
                            particle = n_v  # Success in taking point
                            taken.append(edge)

                else:
                    if particle != end:  # If the particle isn't before the sink, where is it?
                        print("Particle out of range!")
                        return "Error."

        return taken

    # Credit to Daniel Hathcock for the beautiful algorithm
    def generate_unique_minimum(self):
        edges = self.generate_unique_minimum_edges()
        print(edges)
        self.grid = [[0 for j in range(self.boundary_size)] for i in range(self.boundary_size)]
        gradient_grid = [[-1 for j in range(self.boundary_size)] for i in range(self.boundary_size)]

        for x in range(self.boundary_size):  # The correct initialization.
            gradient_grid[x][0] = 1

        for edge in edges:
            if edge[1][0] - edge[0][0] == 1:  # If it is a horizontal transition.
                x = edge[0][0]
                y = edge[0][1]
                gradient_grid[x][y] = 1
            elif edge[1][1] - edge[0][1] == 1:  # If it is a vertical transition.
                x = edge[0][0]
                y = edge[0][1]
                if y == 0:  # It's one of the bottom edges.
                    gradient_grid[x][0] = -1
            else:
                raise "Edge Transitions Error"

        for x in range(1, self.boundary_size):
            self.grid[x][0] = (self.grid[x - 1][0] + gradient_grid[x][0]) % 3

        for x in range(self.boundary_size):
            for y in range(1, self.boundary_size):
                self.grid[x][y] = (self.grid[x][y - 1] + gradient_grid[x][y]) % 3


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
        for x in range(self.boundary_size):  # Are all these -1's right? Somehow, I doubt it...
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