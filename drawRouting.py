import numpy as np
from matplotlib.path import Path
from matplotlib.patches import PathPatch
import matplotlib.pyplot as plt
import copy

import random

epsilon = 0.03

fig, ax = plt.subplots()

lattice_vertices = []
lattice_code = []

for y in range(5):
    lattice_vertices += [(0, y), (5, y)]
lattice_code += [Path.MOVETO, Path.LINETO] * (5)

for x in range(5):
    lattice_vertices += [(x, 0), (x, 5)]
lattice_code += [Path.MOVETO, Path.LINETO] * (5)

lattice_vertices = np.array(lattice_vertices, float)
lattice = Path(lattice_vertices, lattice_code)

lattice_path = PathPatch(lattice, facecolor='None', edgecolor='grey', linestyle='dotted')
ax.add_patch(lattice_path)

###########

vertices = [(1,0), (1,1), (1, 2), (2,2), (2, 3), (2, 3), (3,3), (4,3), (5,3)]
codes = [Path.MOVETO] + (len(vertices) - 1) * [Path.LINETO]  # IMPORTANT LINE OF CODE.

vertices = np.array(vertices, float)
path = Path(vertices, codes)

pink = PathPatch(path, facecolor='None', edgecolor='#F66DD5', linewidth=2.0)

##########

blue_vertices = [(1 + epsilon,0), (1 + epsilon,1 - epsilon), (2 + epsilon,1 - epsilon), (2 + epsilon, 2 - epsilon), (2 + epsilon ,3 - epsilon), (3, 3 - epsilon ), (4, 3 - epsilon ), (5 , 3 - epsilon)]
blue_codes = [Path.MOVETO] + (len(blue_vertices) - 1) * [Path.LINETO]  # IMPORTANT LINE OF CODE.

vertices = np.array(blue_vertices, float)
path = Path(vertices, blue_codes)

blue = PathPatch(path, facecolor='None', edgecolor='blue', linewidth=2.0)

##########

grey_vertices = [(2,2), (3,2), (3,3)]
grey_codes = [Path.MOVETO, Path.LINETO, Path.LINETO]

vertices = np.array(grey_vertices, float)
path = Path(vertices, grey_codes)

grey = PathPatch(path, facecolor='None', edgecolor='#565656', linewidth=2.0, linestyle='--')

ax.add_patch(pink)
ax.add_patch(blue)
ax.add_patch(grey)

ax.set_title('Figure 2')

ax.dataLim.update_from_data_xy(vertices)
ax.set_xlim(0, 5)
ax.set_ylim(0, 5)

plt.show()