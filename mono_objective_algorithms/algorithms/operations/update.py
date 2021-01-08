
from mono_objective_algorithms.algorithms.operations.fitness import fit

#+----------------------------------------------------------------------------------------------+#

def updateBest(solutionsList, best_solution , new_solution = None):
    
    if new_solution == None:  # updating after many solutions are added
        new_solution = max(solutionsList , key = lambda sol:sol.fitness)
        
    if new_solution.fitness > best_solution.fitness :
        best_solution.cp = new_solution.cp
        best_solution.fitness = new_solution.fitness


#+----------------------------------------------------------------------------------------------+#

def updateMinMax(solutionsList, minQos, maxQos , weights , best_solution = None):
    # looking for minQos and maxQos in best_cp
    try:
        best_solution_Qos = best_solution.cp.cpQos()
        for qos in best_solution_Qos:
            if best_solution_Qos[qos] < minQos[qos]:
                minQos[qos] = best_solution_Qos[qos]
            if best_solution_Qos[qos] > maxQos[qos]:
                maxQos[qos] = best_solution_Qos[qos]
    except:  # best_solution not created
        None

    # looking for minQos and maxQos in solutionsList
    for sol in solutionsList:
        qosDict = sol.cp.cpQos()
        for qos in qosDict:
            if qosDict[qos] < minQos[qos]:
                minQos[qos] = qosDict[qos]
            if qosDict[qos] > maxQos[qos]:
                maxQos[qos] = qosDict[qos]

    # Updating best fitness
    try:
        best_solution.fitness = fit(best_solution.cp, minQos, maxQos, weights)
    except:  # best_solution not created
        None

    # updating fitness
        for sol in solutionsList:
            sol.fitness = fit(sol.cp, minQos, maxQos, weights)