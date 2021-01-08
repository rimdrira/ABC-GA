import networkx
import matplotlib.pyplot as plt

from data_structure.Problem import Problem
from mono_objective_algorithms.experimentation.validation_test.hybrid import simABCgenetic


# main

# input
n_act = 5
n_candidates = 50
constraints = {'responseTime': n_act * 5 , 'price': n_act * 3, 'availability': 0.9 ** n_act, 'reliability': 0.7 ** n_act}
weights = [0.25, 0.25, 0.25, 0.25]
mcn = 10
sq = 2
sn = 10

# problem init

p = Problem(n_act , n_candidates , constraints , weights)

# plotting simulation actGraph

positions = {0: [0, 0], 1: [1, 0], 2: [2, 0] , 3: [3, 0], 4: [4, 0]}
G = networkx.DiGraph()
G.add_weighted_edges_from(p.getActGraph())
networkx.drawing.nx_pylab.draw_networkx(G, pos=positions)
plt.show()

# simulation start

simABCgenetic(problem = p , SN=sn, SQ=sq, MCN=mcn, SCP=9 * mcn // 10, N=sn // 2,CP=0.2)
