# ABC-GA
We present in this project the   
The development language used in our work is Python. 

Description of the projects folders: 
- The data structure folder presents: the data structure used in our algorithm to design a composition plan. 
- The  genetic_operations folder: contains the implementation of genetic operations (cross-over and mutation).

- The folder validation_test: Used to set the optimal parameters configuration of our ABC-GA algorithm. 
- the folder evaluation_test: Used to evaluate the performance of ABC-GA algorithm based on several performance metrics ().

The QoS attributes considered in our project are cost,response time, availability and reliability. 
The simulations performed are based on a variation of the values of these attributes in order to generate several solutions. We define the laws of variation ofthese attributes as follows: 
- The cost follows the Uniform law between[0.2,0.95]. 
- Response time follows the Uniform law [20,1500]. 
- Availability follows the Uniform law between[0.9,0.99]. 
- Reliability follows the Uniform Law between[0.7,0.95]
- We assign the weight = 0.25to each quality of service attribute.
