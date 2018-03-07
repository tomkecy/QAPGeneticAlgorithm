import numpy as np

class GeneticAlgorithm:
    def __init__(self, num_of_locations, flow_matrix, distance_matrix):
        self.__num_of_locations = num_of_locations
        self.__flow_matrix = flow_matrix
        self.__distance_matrix = distance_matrix

    def __generate_specimen(self):
        specimen = [i for i in range(1, self.__num_of_locations + 1)]
        np.random.shuffle(specimen)
        return specimen

    def initialise_population(self, population_size):
        population = np.array([self.__generate_specimen() for _ in range(0, population_size)])
        return population

    def evaluate(self, population):
        return np.array(
            [self.evaluate_specimen_fitness(specimen) for specimen in population]
        )

    def run(self, population_size, generations):
        current_generation = 0
        population = self.initialise_population(population_size)
        population_fitness = self.evaluate(population)

        while current_generation < generations:
            population = self.selection(population, population_fitness)
            population = self.crossover(population)
            current_generation += 1
        return population

    def evaluate_specimen_fitness(self, specimen):
        fitness_acc = 0
        for facility in range(0, len(specimen)):
            for other_facility in range(0, len(specimen)):
                if facility == other_facility:
                    continue
                fitness_acc += self.__flow(facility, other_facility) * self.__distance(specimen[facility], specimen[other_facility])
        return fitness_acc


    def selection(self, population, population_fitness):
        return np.array(
            [population[i] if population_fitness[i] <= population_fitness[i+1] else population[i+1]
             for i in range(0, len(population), 2)]
        )

    def crossover(self, population):
        pass

    def __distance(self, location, other_location):
        return self.__distance_matrix[location-1, other_location-1]

    def __flow(self, facility, other_facility):
        return self.__flow_matrix[facility, other_facility]




