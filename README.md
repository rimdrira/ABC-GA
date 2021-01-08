We present in this repository the source code (Python) of our ABC-GA algorithm and the corresponding test dans simulation code. ABC-GA is an Artificial Bee Colony (ABC) based algorithm using genetic operations from the Genetic Algorithm (GA). ABC-GA resolves the optimized selection of the best composition of cloud services with regard to business and QoS requirements.  

Description of the main folders:

ABC-GA/data_structure/ presents the data structure used in our algorithm to design a composition plan.
ABC-GA/genetic_operations/ contains the implementation of genetic operations (cross-over and mutation).
ABC-GA/mono_objective_algorithms/ contains the implementation of ABC-GA and algorithms compared to ABC-GA in the evaluation test.
ABC-GA/mono_objective_algorithms/experimentation/validation_test/ is used to set the optimal parameters configuration of our ABC-GA algorithm.
ABC-GA/mono_objective_algorithms/experimentation/evaluation_test/ is used to evaluate the performance of ABC-GA algorithm based on several performance metrics (Optimality, Convergence, Scalability).

The QoS attributes considered in our project are cost,response time, availability and reliability. The simulations performed are based on a variation of the values of these attributes in order to generate several solutions. We define the laws of variation ofthese attributes as follows:

The cost follows the Uniform law between[0.2,0.95].
Response time follows the Uniform law [20,1500].
Availability follows the Uniform law between[0.9,0.99].
Reliability follows the Uniform Law between[0.7,0.95]
We assign the weight = 0.25 to each quality of service attribute.

If you have any questions please contact us.

Contact info: Rim DRIRA: rim.drira@ensi-uma.tn
