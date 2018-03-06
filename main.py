from data_reader import *
from genetic_algorithm import *

pop_size = 100
gen = 100
Px = 0.7
Pm = 0.01
Tour = 5

reader = DataReader()
n, flow_matrix, distance_matrix = reader.read_data("data/had12.dat")

genetic_algorithm = GeneticAlgorithm(n, flow_matrix, distance_matrix)
#print(genetic_algorithm.run(2, gen))
print(genetic_algorithm.evaluate_specimen_fitness([3,10,11,2,12,5,6,7,8,1,4,9]))
