from numpy.random import uniform , choice 
from data_structure.Service import Service

#+----------------------------------------------------------------------------------------------+#

def generateActGraph(n_act):  # Sequencial 
    return [[i, i + 1, 0] for i in range(n_act - 1)]


#+----------------------------------------------------------------------------------------------+#



def generateCandidates(n_act, n_candidates):  # Randomly generated candidates 
    candidates = list()
    state = ["over", "precise"]
    for i in range(n_act):
        candidates.append([])
        for j in range(n_candidates):
            responseTime = uniform(0.1, 5, 1)[0]
            price = uniform(0.1, 3, 1)[0]
            availability = uniform(0.9, 0.99, 1)[0]
            reliability = uniform(0.7, 0.95, 1)[0]
            matchingState = choice(state)
            service = Service(i, responseTime, reliability, availability, price, matchingState)
            if matchingState == "precise":
                candidates[i].append(service)
            candidates[i].append(service)
    return candidates