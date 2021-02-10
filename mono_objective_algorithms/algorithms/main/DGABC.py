from math import inf
from random import sample, randint, random
from data_structure.CompositionPlan import CompositionPlan
from data_structure.Solution import Solution
from genetic_operations.implementation import mutate
from mono_objective_algorithms.algorithms.operations.fitness import fit 
from mono_objective_algorithms.algorithms.operations.update import updateBest , updateMinMax

def chooseNeighbor(sol , problem , best_solution) :
    service = sol.cp.randomService()
    xi = problem.getCandidates()[service.getActivity()].index(service)
    N = len(problem.getCandidates()[service.getActivity()]) - 1
    y = best_solution.cp.getService(service.getActivity())
    yi = problem.getCandidates()[service.getActivity()].index(y)
    vi = xi + randint(-1, 1) * (xi - randint(0, N)) + randint(0, 2) * (yi - xi)
    vi = max(vi, 0)
    vi = min(N, vi)
    return problem.getCandidates()[service.getActivity()][vi]

# SN : n of ressources , SQ : condition for scouts , MCN : number of iterations , N : n of bees 

def DGABC(problem, SN, SQ, MCN, N):

    # solutions initializing
    solutionsList = list()
    plotx = []
    
    minQos = {'responseTime': inf, 'price': inf, 'availability': inf, 'reliability': inf}
    maxQos = {'responseTime': 0, 'price': 0, 'availability': 0, 'reliability': 0}

    for i in range(SN):
        while 1:
            cp = CompositionPlan(problem.getActGraph(), problem.getCandidates())
            if cp.verifyConstraints(problem.getConstraints()):
                solutionsList.append(Solution(cp = cp , fitness = 0 , probability = 0 , limit = 0))
                break

    # minQos maxQos and fitness initializing
    updateMinMax(solutionsList , minQos, maxQos , problem.getWeights())


    # initializing best_solution
    best_solution = max(solutionsList , key = lambda sol:sol.fitness)

    #+----------------------------------------------------------------------------------------------+#


    conv_itera = 1
    # Algorithm
    for itera in range(MCN):
        print(f"Completed = {((itera+1)/MCN)*100:.2f}%" , end = '\r')
        prev_opt = best_solution.fitness
        # employed bees phase
        exploited = sample(solutionsList, N)  # Generating positions list for exploitation
        for sol in exploited:
            while 1:
                    # choose randomly a service to mutate
                    neighbor = chooseNeighbor(sol , problem , best_solution)
                    # mutation operation
                    new = mutate(sol.cp, neighbor)
                    if new.verifyConstraints(problem.getConstraints()):
                        new_fitness = fit(new, minQos, maxQos, problem.getWeights())
                        # checking if new fitness is better than parent fitness
                        if new_fitness > sol.fitness:
                            sol.cp = new
                            sol.fitness = new_fitness 
                            sol.probability = 0 
                            sol.limit = 0
                        else:
                            sol.limit += 1
                        break

        # end of employed bees phase

        updateBest(solutionsList, best_solution)

        # Probability update
        for sol in exploited:
            sol.probability = (sol.fitness * 0.9 / max([sol.fitness for sol in solutionsList])) * 0.1

        # onlooker bees phase
        for sol in exploited:
            if random() <= sol.probability  :
                # choose randomly a service to mutate
                neighbor = chooseNeighbor(sol , problem , best_solution)
                # mutation operation
                new = mutate(sol.cp, neighbor)
                if new.verifyConstraints(problem.getConstraints()):
                    new_fitness = fit(new, minQos, maxQos, problem.getWeights())
                    # checking if new fitness is better than parent fitness
                    if new_fitness > sol.fitness:
                        sol.cp = new
                        sol.fitness = new_fitness
                        sol.probability = 0
                        sol.limit = 0
                    else:
                        sol.limit += 1
                    break
        # end of onlooker bees phase

        # scout bees phase
        for sol in exploited:
            if sol.limit >= SQ:  # verifying scouts condition
                # searching for new ressources to exploit
                while 1:
                    r = CompositionPlan(problem.getActGraph(), problem.getCandidates())
                    if r.verifyConstraints(problem.getConstraints()):
                        sol.cp = r
                        sol.fitness = fit(sol.cp, minQos, maxQos, problem.getWeights())
                        sol.probability = 0
                        sol.limit = 0
                        break

        
    
            
        # end of scout bees phase

        updateBest(solutionsList, best_solution)

        # this segment is used for calculating conv 
        if best_solution.fitness - prev_opt > 0.0001 :
            conv_itera = itera+1

        updateMinMax(solutionsList, minQos, maxQos , problem.getWeights() , best_solution)
        plotx.append(best_solution.cp)
        
        
    
    # end of algorithm
    print("")
    return best_solution.cp , minQos , maxQos , conv_itera,plotx
