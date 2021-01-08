from math import inf
from random import sample, uniform , random
from numpy.random import choice
from data_structure.CompositionPlan import CompositionPlan
from data_structure.Solution import Solution
from genetic_operations.implementation import crossover, mutate
from mono_objective_algorithms.algorithms.operations.fitness import fit 
from mono_objective_algorithms.algorithms.operations.update import updateBest , updateMinMax


#+----------------------------------------------------------------------------------------------+#


# G : n of generations  , N : size of population
# CP : crossover probability , CM : mutation probability

def genetic(problem, N, G, CP, CM):

    # population initializing
    population = list()
    plotx = []
    
    minQos = {'responseTime': inf, 'price': inf, 'availability': inf, 'reliability': inf}
    maxQos = {'responseTime': 0, 'price': 0, 'availability': 0, 'reliability': 0}

    for i in range(N):
        while 1:
            cp = CompositionPlan(problem.getActGraph(), problem.getCandidates())
            if cp.verifyConstraints(problem.getConstraints()):
                population.append(Solution(cp = cp , fitness = 0 , probability = 0))
                break

    # minQos maxQos and fitness initializing
    updateMinMax(population , minQos, maxQos , problem.getWeights())


    #+----------------------------------------------------------------------------------------------+#

    conv_itera = 1
    # Algorithm
    for generation in range(G):

        prev_opt = population[0].fitness

        # Probability update
        s = sum([indiv.fitness for indiv in population])
        for indiv in population:
            indiv.probability = indiv.fitness / s

        probabilityList = [indiv.probability for indiv in population]
        a = min(probabilityList)
        b = max(probabilityList)
        parents = []
        # Selecting best individuals
        n_individuals = 0
        while n_individuals < 2 : 
            for indiv in population:
                if indiv.probability >= uniform(a,b):
                    n_individuals += 1 
                    parents.append(indiv)
        
        # Mating selection
        parent1 , parent2 =  sample(parents , 2)

        while 1:
            offspring = crossover(parent1.cp, parent2.cp, CP)  # Recombining
            if random() <= CM : # Mutation
                service = offspring.randomService()
                while 1:
                    random_service = choice(problem.getCandidates()[service.getActivity()])
                    if random_service != service:
                        break
                offspring = mutate(offspring, random_service)
            if offspring.verifyConstraints(problem.getConstraints()):
                offspring_fitness = fit(offspring, minQos, maxQos, problem.getWeights())
                offspring_solution = Solution(cp = offspring , fitness = offspring_fitness , probability = 0)
                break
        
        # Adding offsprings
        population.append(offspring_solution)

        # Keeping best individuals
        population = sorted(population, key = lambda indiv : indiv.fitness , reverse=True)[:N]

        # this segment is used for calculating conv 
        if population[0].fitness - prev_opt > 0.0001 :
            conv_itera = generation + 1

        updateMinMax(population , minQos, maxQos , problem.getWeights())
        plotx.append(population[0].cp)
    
    # end of algorithm
    return population[0].cp , minQos , maxQos , conv_itera,plotx
