import time
import csv
import multiprocessing
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

from data_structure.Problem import Problem
from mono_objective_algorithms.algorithms.main.hybrid import ABCgenetic
from mono_objective_algorithms.algorithms.main.ABC import ABC
from mono_objective_algorithms.algorithms.main.genetic import genetic
from mono_objective_algorithms.algorithms.operations.fitness import fit
from numpy import zeros, array


def evaluate(algorithm,opt,weights,n_act, n_candidates, sn, mcn, sq,F,K, **kwargs):
    rt_list = []
    cp_list = []
    min_list = []
    max_list = []
    conv_list = []
    CP_PLOT = []
    for itera in range(30):
        print(f"Executing Algorithm : {algorithm.__name__} {itera + 1}/30")
        start_time = time.time()
        result, minQos, maxQos, conv_itera, plotx = algorithm(**kwargs)
        CP_PLOT.append(plotx)
        rt = time.time() - start_time
        rt_list.append(rt)
        min_list.append(minQos)
        max_list.append(maxQos)
        cp_list.append(result)
        conv_list.append(conv_itera)

    minQos_avg = {qos: sum([cp_qos[qos] / 30 for cp_qos in min_list]) for qos in opt.cpQos().keys()}
    maxQos_avg = {qos: sum([cp_qos[qos] / 30 for cp_qos in max_list]) for qos in opt.cpQos().keys()}
    opt_fit = fit(opt, minQos_avg, maxQos_avg, weights)
    k = zeros(mcn,)
    for l in CP_PLOT:
        k += array([fit(cp,minQos,maxQos,weights) for cp in l]) / (opt_fit*30)
    fit_list = [fit(cp, minQos_avg, maxQos_avg, weights) / opt_fit for cp in cp_list]
    fit_avg = sum(fit_list) / 30
    rt_avg = sum(rt_list) / 30

    div = 0
    conv = sum(conv_list) // 30
    for i in range(len(fit_list) - 1):
        div += abs(fit_list[i + 1] - fit_list[i]) / 29

    with open('test_results.csv', mode='a') as file:
        file_writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        if (algorithm.__name__ == "ABCgenetic" or algorithm.__name__ == "ABC"):
            file_writer.writerow([algorithm.__name__, n_act, n_candidates, sn, mcn, sq, fit_avg, rt_avg, div, conv])
        else:
            file_writer.writerow([algorithm.__name__, n_act, n_candidates, sn, mcn, "__", fit_avg, rt_avg, div, conv])

    F[algorithm.__name__] = fit_list
    K[algorithm.__name__] = k


# main
if __name__ == "__main__":
    # input
    n_act = int(input("NUMBER OF ACTIVITIES : "))
    n_candidates = int(input("NUMBER OF CANDIDATE SERVICES : "))
    constraints = {'responseTime': n_act * 2 , 'price': n_act * 3, 'availability': 0.92 ** n_act, 'reliability': 0.75 ** n_act}
    weights = [0.5, 0.1, 0.15, 0.25]
    mcn = int(input("ITERATION NUMBER / GENERATION NUMBER : "))
    sn = int(input("RESSOURCES NUMBER / POPULATION SIZE : "))
    sq = int(input("SCOUTS CONDITION : "))

    # problem init

    p = Problem(n_act, n_candidates, constraints, weights)

    # optimal fitness

    print("optimal fitness search !")
    opt, _, _, _, _ = ABCgenetic(problem=p, SN=sn, SQ=100, MCN=mcn * 10, SCP=9 * mcn // 10, N=sn // 2, CP=0.2)
    print("\nDone !")

    # test scenarios

    manager1 = multiprocessing.Manager()
    F = manager1.dict()
    manager2 = multiprocessing.Manager()
    K = manager2.dict()

    L = [ (ABCgenetic ,{'problem': p, 'SN': sn, 'SQ': sq, 'MCN': mcn, 'SCP': 9 * mcn // 10, 'N': sn // 2, 'CP': 0.2}),
           (ABC ,{'problem': p, 'SN': sn, 'SQ': sq, 'MCN': mcn, 'N': sn // 2}),
           (genetic, {'problem': p, 'N': sn, 'G': mcn, 'CP': 0.75, 'CM': 0.1})]

    processes = []
    for parameters in L:
        p = multiprocessing.Process(target=evaluate, args=(parameters[0],opt,weights,n_act, n_candidates, sn, mcn, sq,F,K) , kwargs = parameters[1])
        processes.append(p)
        p.start()

    for p in processes:
       p.join()

    K1 = K['ABCgenetic']
    K2 = K['ABC']
    K3 = K['genetic']
    fit_list = F['ABCgenetic'] + F['ABC'] + F['genetic']

    #plot boxplot section
    d = {"fitness": fit_list , f"scenario({n_act},{n_candidates})": [" ABCgenetic"]*30 + [" ABC"]*30 + [" genetic"]*30 }
    df = pd.DataFrame(data=d)
    print(df)
    sns_plot = sns.boxplot(x =f"scenario({n_act},{n_candidates})" ,y ="fitness", data=df)
    plt.title(f" Scenario: Num_Act:{n_act},Num_candidates{n_candidates}, MCN:{mcn},SN{sn},SQ:{sq}")
    sns_plot.figure.savefig(f"boxplots/boxplot({n_act},{n_candidates},{mcn},{sn},{sq}).png")

    # plot iterations

    plt.clf()
    plt.plot([i for i in range(1, mcn + 1)], K1, label='ABCgenetic')
    plt.plot([i for i in range(1, mcn + 1)], K2, label='ABC')
    plt.plot([i for i in range(1, mcn + 1)], K3, label='Genetic')
    plt.legend()
    plt.xlabel('iterations')
    plt.ylabel('Average fitness')
    plt.title(f" Scenario: Num_Act:{n_act},Num_candidates{n_candidates}, MCN:{mcn},SN{sn},SQ:{sq}")
    plt.savefig(f"convergence_plots/plot({n_act},{n_candidates},{mcn},{sn},{sq}).png")
