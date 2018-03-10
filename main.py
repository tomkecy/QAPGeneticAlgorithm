from data_logger import DataLogger
from data_reader import *
from genetic_algorithm import *

pop_size = 100
gen = 100
Px = 0.7
Pm = 0.01
Tour = 5

reader = DataReader()
n, flow_matrix, distance_matrix = reader.read_data("data/had12.dat")
logger = DataLogger()

genetic_algorithm = GeneticAlgorithm(n, pop_size, flow_matrix, distance_matrix, Pm, Px, Tour, logger)
print(genetic_algorithm.run(gen))
logger.close()

