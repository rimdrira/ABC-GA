from random import random, randint
from numpy.random import choice


# +----------------------------------------------------------------------------------------------+#

# mutation
def mutate(cp, new_service):
    new_cp = cp.clone()
    # new_service is added to the composition plan
    new_cp.G.nodes[new_service.getActivity()]["service"] = new_service
    return new_cp


# +----------------------------------------------------------------------------------------------+#

# Crossover
def crossover(parent1, parent2, pc):
    offspring = parent1.clone()
    # modifying offspring
    for act in offspring.G.nodes:  # Selecting service to replace
        if random() <= pc:  # pc : probability of crossover
            # replacing with service from second parent
            offspring.G.nodes[act]["service"] = parent2.G.nodes[act]["service"]
    return offspring


# +----------------------------------------------------------------------------------------------+#
# BSG
def BSG(cp1, cp2, constraints, candidates):  # constraints are added to avoid creating offsprings in vain

    def crossover(cp1, cp2):

        offspring1 = cp1.clone()
        offspring2 = cp2.clone()
        attempts = 0
        while 1:
            attempts += 1
            if attempts == 10:
                break
            x1 = randint(0, cp1.getNumberOfActivities() - 2)
            x2 = randint(x1 + 1, cp1.getNumberOfActivities() - 1)
            for act in range(x1, x2 + 1):  # Selecting service to replace
                # replacing with service from second parent
                offspring1.G.nodes[act]["service"] = cp2.G.nodes[act]["service"]
                offspring2.G.nodes[act]["service"] = cp1.G.nodes[act]["service"]
            if offspring1.verifyConstraints(constraints) and offspring2.verifyConstraints(constraints):
                break

        return [offspring1, offspring2]

    def mutate(cp):

        offspring = cp.clone()

        # choose randomly a service to mutate
        service = offspring.randomService()
        attempts = 0
        while 1:
            attempts += 1
            if attempts == 10:
                break
            while 1:
                new = choice(candidates[service.getActivity()])
                if new != service:
                    break
            # mutation operation
            offspring.G.nodes[new.getActivity()]["service"] = new
            if offspring.verifyConstraints(constraints):
                break

        return offspring

    offspringsList = []

    # Crossover

    # First and second offsprings

    offspringsList.extend(crossover(cp1, cp2))

    # Mutation

    # third offspring

    while 1:
        offspring = mutate(cp1)
        if offspring not in offspringsList:
            break

    offspringsList.append(offspring)

    # fourth offspring

    while 1:
        offspring = mutate(cp2)
        if offspring not in offspringsList:
            break

    offspringsList.append(offspring)

    return offspringsList

# +----------------------------------------------------------------------------------------------+#
# Rim DRIRA
def generateOffsprings (cp1, cp2, constraints, candidates):  # constraints are added to avoid creating offsprings in vain

    offspringsList = []

    # Crossover
    pc=0.5
    res=crossover(cp1,cp2, pc)
    offspringsList.append(res)

    # Mutation
    def mutate(cp):
        abandon = 0              # ADDED ABANDON CRITERIA
        offspring = cp.clone()

        # choose randomly a service to mutate
        service = offspring.randomService()
        while 1:
            abandon += 1
            while 1:
                new = choice(candidates[service.getActivity()])
                if new != service:
                    break
            # mutation operation
            offspring.G.nodes[new.getActivity()]["service"] = new
            if offspring.verifyConstraints(constraints) or abandon > 10 :
                break

        return offspring

    # second offspring

    while 1 : 
        offspring = mutate(res)
        if offspring not in offspringsList : 
            break
        
    offspringsList.append(offspring)

    # third offspring

    #while 1 :
        #offspring = mutate(cp2)
        #if offspring not in offspringsList :
            #break
        
    #offspringsList.append(offspring)

    return offspringsList
