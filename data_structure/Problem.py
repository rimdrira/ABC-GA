
from data_structure.generate import generateActGraph , generateCandidates

#+----------------------------------------------------------------------------------------------+#


class Problem:

    # constructor

    def __init__(self, n_act , n_candidates , constraints , weights = None):
        self.__actGraph = generateActGraph(n_act)
        self.__candidates = generateCandidates(n_act , n_candidates) 
        self.__weights = weights
        self.__constraints = constraints

    # get attributs

    def getActGraph(self):
        return self.__actGraph

    def getCandidates(self):
        return self.__candidates

    def getWeights(self):
        return self.__weights

    def getConstraints(self):
        return self.__constraints