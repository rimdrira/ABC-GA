from random import uniform, randint, sample, random
from math import inf
from prettytable import PrettyTable
from data_structure.CompositionPlan import CompositionPlan
from data_structure.Solution import Solution
from genetic_operations.implementation import crossover, mutate
from mono_objective_algorithms.algorithms.operations.fitness import fit
from mono_objective_algorithms.algorithms.operations.update import updateBest, updateMinMax


# SN : n of ressources  , SQ : condition for scouts , MCN : number of iterations
# N : n of bees , CP : crossover probability , SCP : scout bees changing point

def simABCgenetic(problem, SN, SQ, MCN, SCP, N, CP):
    print(f"SN = {SN} , SQ = {SQ} , MCN = {MCN} , N = {N} , CP = {CP}")

    def show_solutions():
        t = PrettyTable(['solution', 'fitness', 'probability', 'limit'])
        for sol in solutionsList:
            t.add_row([sol.number, sol.fitness, sol.probability, sol.limit])
        t.add_row(["best_cp", best_solution.fitness, "", ""])
        print(t)

    def show_solution(cp):
        t = PrettyTable(['activity', 'price', 'responseTime', 'availability', 'reliability', 'matching'])
        for i in range(cp.getNumberOfActivities()):
            t.add_row([i, cp.getService(i).getPrice(), cp.getService(i).getResponseTime(),
                       cp.getService(i).getAvailability(), cp.getService(i).getReliability(),
                       cp.getService(i).getMatching()])
        print(t)

    ############################# Algorithm start  ##################################
    print("Initialzing ...")

    # solutions initializing
    solutionsList = list()

    minQos = {'responseTime': inf, 'price': inf, 'availability': inf, 'reliability': inf}
    maxQos = {'responseTime': 0, 'price': 0, 'availability': 0, 'reliability': 0}

    for i in range(SN):
        while 1:
            cp = CompositionPlan(problem.getActGraph(), problem.getCandidates())
            if cp.verifyConstraints(problem.getConstraints()):
                solutionsList.append(Solution(cp=cp, fitness=0, probability=0, limit=0, number=i + 1))
                break

    # minQos maxQos and fitness initializing
    updateMinMax(solutionsList, minQos, maxQos, problem.getWeights())

    # initializing best_solution
    best_solution = max(solutionsList, key=lambda sol: sol.fitness)

    show_solutions()

    print("algorithm start")
    print("employed bees phase ...")

    # +----------------------------------------------------------------------------------------------+#

    # Algorithm
    for itera in range(MCN):
        print(f"iteration = {itera + 1}")
        # employed bees phase
        exploited = sample(solutionsList, N)  # Generating positions list for exploitation
        print(f"exploited solutions = {[sol.number for sol in exploited]}")
        for sol in exploited:
            print(f"solution {sol.number} chosen ... ")
            show_solution(sol.cp)
            while 1:
                random = CompositionPlan(problem.getActGraph(), problem.getCandidates())  # randomly generated cp
                print("generating random plan")
                show_solution(random)
                offspring = crossover(sol.cp, random, CP)  # Crossover operation
                print("crossover execution !")
                show_solution(offspring)
                if offspring.verifyConstraints(problem.getConstraints()):
                    new_fitness = fit(offspring, minQos, maxQos, problem.getWeights())
                    print(f"new_fitness = {new_fitness}")
                    print(f"old_fitness = {sol.fitness}")
                    if new_fitness > sol.fitness:  # checking if offspring fitness is better than parent fitness
                        sol.cp = offspring
                        sol.fitness = new_fitness
                        sol.probability = 0
                        sol.limit = 0
                        print("replaced !")
                    else:
                        sol.limit += 1
                        print("not replaced !")
                    break
        # end of employed bees phase

        updateBest(solutionsList, best_solution)
        print("updating best !")
        print("onlooker bees phase ...")

        # Probability update
        s = sum([sol.fitness for sol in solutionsList])
        for sol in exploited:
            sol.probability = sol.fitness / s

        # onlooker bees phase
        probabilityList = [sol.probability for sol in solutionsList]
        a = min(probabilityList)
        b = max(probabilityList)
        for sol in exploited:
            print(f"solution {sol.number} chosen ... ")
            r = uniform(a, b)
            print(f"probability = {sol.probability} vs random = {r}")
            if sol.probability > r:
                "selected by probability !"
                show_solution(sol.cp)
                print("crossover with best_cp")
                show_solution(best_solution.cp)
                while 1:
                    offspring = crossover(sol.cp, best_solution.cp, CP)  # Crossover operation
                    print("crossover execution !")
                    show_solution(offspring)
                    if offspring.verifyConstraints(problem.getConstraints()):
                        new_fitness = fit(offspring, minQos, maxQos, problem.getWeights())
                        print(f"new_fitness = {new_fitness}")
                        print(f"old_fitness = {sol.fitness}")
                        if new_fitness > sol.fitness:  # checking if offspring fitness is better than parent fitness
                            sol.cp = offspring
                            sol.fitness = new_fitness
                            sol.probability = 0
                            sol.limit = 0
                            print("replaced !")
                            updateBest(solutionsList, best_solution, sol)
                        else:
                            sol.limit += 1
                            print("not replaced !")
                        break
        # end of onlooker bees phase
        print("scouts bees phase ...")
        show_solutions()
        # scout bees phase
        for sol in exploited:
            if sol.limit >= SQ:  # verifying scouts condition
                print(f"solution {sol.number} reached limit ... ")
                if itera >= SCP:  # change of scouts behaviour condition to mutating
                    show_solution(sol.cp)
                    while 1:
                        # choose randomly a service to mutate
                        x = randint(0, sol.cp.getNumberOfActivities() - 1)
                        service = sol.cp.getService(x)
                        print(f"the service of activity {x} will be mutated")
                        neighborsList = problem.getCandidates()[service.getActivity()]
                        neighbor = service.getNeighbor(neighborsList)
                        # mutation operation
                        new = mutate(sol.cp, neighbor)
                        print("mutation execution !")
                        if new.verifyConstraints(problem.getConstraints()):
                            show_solution(new)
                            sol.cp = new
                            sol.fitness = fit(new, minQos, maxQos, problem.getWeights())
                            sol.probability = 0
                            sol.limit = 0
                            break

                else:  # searching for new ressources to exploit
                    while 1:
                        print("generating random solution instead !")
                        random = CompositionPlan(problem.getActGraph(), problem.getCandidates())
                        if random.verifyConstraints(problem.getConstraints()):
                            show_solution(random)
                            sol.cp = random
                            sol.fitness = fit(cp, minQos, maxQos, problem.getWeights())
                            sol.probability = 0
                            sol.limit = 0
                            break
        # end of scout bees phase
        updateMinMax(solutionsList, minQos, maxQos, problem.getWeights(), best_solution)
        updateBest(solutionsList, best_solution)
        print("end of iteration")
        show_solutions()

    print("end of algorithm")
    # end of algorithm
