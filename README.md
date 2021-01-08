We present in this project the evaluation of our work. This evaluation is based on several simulations. Our simulation consists of two parts. We set, firstly, the optimal parameters configuration of our ABC-GA algorithm that provides the optimal solution. This part is implemented in the folder validation_test.
Second, we evaluate the performance of the ABC-GA algorithm based on several performance metrics. This part is implemented in the folder evaluation_test.
The data structure folder present the data structure used in our algorithm to design a composition plan.
We implement genetic operation (cross-over and mutation) in the folder genetic_operations.
All the simulations carried out in our work are executed on a machine whose characteristics are:
•Processor: 2.9 GHz Intel Core i5 dual core.
•RAM capacity: 8GB.
•Operating system: Mac OS.
The development language used in our work is Python. 
The QoS attributes considered in our simulations are cost,response time, availability and reliability. The simulations performed are based on a variation of the values of theseattributes in order to generate several solutions. We define the laws of variation ofthese attributes as follows: The cost follows the Uniform law between[0.2,0.95]. Response time follows the Uniform law [20,1500]. Availability follows the Uniform law between[0.9,0.99]. Reliability follows the Uniform Law between[0.7,0.95] We assign the weight = 0.25to each quality of service attribute.
