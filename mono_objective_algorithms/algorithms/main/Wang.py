from math import inf
from random import sample, uniform , random , randint
from numpy.random import choice
from numpy import array
from data_structure.CompositionPlan import CompositionPlan
from data_structure.Solution import Solution
from genetic_operations.implementation import mutate
from mono_objective_algorithms.algorithms.operations.fitness import fit 
from mono_objective_algorithms.algorithms.operations.update import updateMinMax


#+----------------------------------------------------------------------------------------------+#

def nonDominated(cp1 , L) :
    cp1_array = array([*cp1.cpQos()])
    result = True
    for cp2 in L :
        if not result:
            break
        cp2_array = array([*cp2.cp.cpQos()])
        if (cp2_array >= cp1_array).all() and (cp2_array > cp1_array).any():
            result = False
    return result

def dominates(cp1 , L) :
    cp1_array = array([*cp1.cpQos()])
    result = False
    for cp2 in L :
        if result:
            break
        cp2_array = array([*cp2.cp.cpQos()])
        if (cp1_array >= cp2_array).all() and (cp1_array > cp2_array).any():
            result = True
    return result


def crossover(cp1, cp2) :

        offspring1 = cp1.clone()
        offspring2 = cp2.clone()

        x1 = randint(0, cp1.getNumberOfActivities())
        for act in range(x1, cp1.getNumberOfActivities()):  # Selecting service to replace
            # replacing with service from second parent
            offspring1.G.nodes[act]["service"] = cp2.G.nodes[act]["service"]
            offspring2.G.nodes[act]["service"] = cp1.G.nodes[act]["service"]

        return [offspring1 , offspring2]

# G : n of generations  , N : size of population
# CP : crossover probability , CM : mutation probability

def Wang(problem, N, G, CM ,CP):

    # population initializing
    population = list()
    plotx = []
    
    minQos = {'responseTime': inf, 'price': inf, 'availability': inf, 'reliability': inf}
    maxQos = {'responseTime': 0, 'price': 0, 'availability': 0, 'reliability': 0}

    for i in range(4 * N // 5):
        while 1:
            cp = CompositionPlan(problem.getActGraph(), problem.getCandidates())
            if cp.verifyConstraints(problem.getConstraints()):
                population.append(Solution(cp = cp , fitness = 0 , probability = 0))
                break

    non_dominated = []
    for i in range(4 * N // 5 , N):
        while 1 :
            cp = CompositionPlan(problem.getActGraph(), problem.getCandidates())
            if cp.verifyConstraints(problem.getConstraints()) and nonDominated(cp , population) and not dominates(cp,non_dominated):
                non_dominated.append(Solution(cp=cp, fitness=0, probability=0))
                break

    population.extend(non_dominated)
    # minQos maxQos and fitness initializing
    updateMinMax(population , minQos, maxQos , problem.getWeights())


    #+----------------------------------------------------------------------------------------------+#

    conv_itera = 1
    # Algorithm
    for generation in range(G):

        print(f"Completed = {((generation+1)/G)*100:.2f}%" , end = '\r')

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
        selected = []
        for parent in parents :
            if random() <= CP :
                selected.append(parent)
                if len(selected) == 2 :
                    break

        parent1 , parent2 = selected


        offsprings = crossover(parent1.cp, parent2.cp)  # Recombining
        for offspring in offsprings :
            if random() <= CM : # Mutation
                service = offspring.randomService()
                while 1:
                    random_service = choice(problem.getCandidates()[service.getActivity()])
                    if random_service != service:
                        break
                offspring = mutate(offspring, random_service)

            offspring_fitness = fit(offspring, minQos, maxQos, problem.getWeights())
            # Adding offsprings
            population.append(Solution(cp = offspring , fitness = offspring_fitness , probability = 0))

        

        # Keeping best individuals
        population = sorted(population, key = lambda indiv : indiv.fitness , reverse=True)[:N]

        # this segment is used for calculating conv 
        if population[0].fitness - prev_opt > 0.0001 :
            conv_itera = generation + 1

        updateMinMax(population , minQos, maxQos , problem.getWeights())
        plotx.append(population[0].cp)
    
    # end of algorithm
    print("")
    return population[0].cp , minQos , maxQos , conv_itera,plotx
