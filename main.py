from data_logger import DataLogger
from data_reader import *
from genetic_algorithm import *

pop_size = 100
gen = 1000
Px = 0.7
Pm = 0.01
Tour = 5
selection = 'tournament'


for i in range(12, 13, 2):
    reader = DataReader()
    n, flow_matrix, distance_matrix = reader.read_data("data/had%s.dat" % str(i))
    logger = DataLogger('had%s_Px%s' % (str(i), Px))
    logger.write_header(pop_size, gen, Px, Pm, Tour, selection)
    for j in range(0, 1):
        genetic_algorithm = GeneticAlgorithm(n, pop_size, flow_matrix, distance_matrix, Pm, Px, Tour, logger, selection)
        print('Had%s file best result: %s' % (i, genetic_algorithm.run(gen)))
    logger.close()


