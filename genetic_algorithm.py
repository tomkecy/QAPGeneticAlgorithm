import numpy as np
from numba import jit


@jit
def _evaluate_specimen_fitness(specimen, flow_matrix, distance_matrix):
    fitness_acc = 0
    for facility in range(0, len(specimen)):
        for other_facility in range(0, len(specimen)):
            if facility == other_facility:
                continue
            fitness_acc += flow_matrix[facility, other_facility] * distance_matrix[
                specimen[facility] - 1,
                specimen[other_facility] - 1]
    return fitness_acc


class GeneticAlgorithm:
    def __init__(self, num_of_locations, pop_size, flow_matrix, distance_matrix, mutation_probability,
                 crossover_probability, tour, data_logger, selection_method='tournament'):
        self.__num_of_locations = num_of_locations
        self.__flow_matrix = flow_matrix
        self.__distance_matrix = distance_matrix
        self.__pop_size = pop_size
        self.__pop_indices_array = np.array([i for i in range(pop_size)])

        self.__data_logger = data_logger
        self.__mutation_probability = mutation_probability
        self.__tour = tour
        self.__crossover_probability = crossover_probability
        self.__population = np.empty(shape=(1, 1))
        self.__population_fitness = np.empty(shape=(1, 1))

        if selection_method.lower() == 'tournament':
            self.__selection_method = self.__tournament_selection
        elif selection_method.lower() == 'roulette':
            self.__selection_method = self.__roulette_selection
        else:
            raise Exception('Not supported selection method')

    def run(self, generations):
        current_generation = 1
        self.__initialise_population()
        self.__evaluate()

        current_best_specimen, current_best_fitness = self.__get_current_best()
        global_best_specimen, global_best_fitness = current_best_specimen, current_best_fitness

        self.__data_logger.write_log(current_generation, current_best_fitness, np.average(self.__population_fitness),
                                     np.amax(self.__population_fitness))

        while current_generation < generations:
            self.__selection()
            self.__crossover()
            self.__mutation()

            self.__evaluate()

            current_best_specimen, current_best_fitness = self.__get_current_best()
            current_generation += 1
            self.__data_logger.write_log(current_generation, current_best_fitness,
                                         np.average(self.__population_fitness),
                                         np.amax(self.__population_fitness))

            if current_best_fitness < global_best_fitness:
                global_best_fitness = current_best_fitness
                global_best_specimen = current_best_specimen

        return global_best_specimen, global_best_fitness

    def __initialise_population(self):
        self.__population = np.array([self.__generate_specimen() for _ in range(0, self.__pop_size)])

    def __generate_specimen(self):
        specimen = [i for i in range(1, self.__num_of_locations + 1)]
        np.random.shuffle(specimen)
        return specimen

    def __get_current_best(self):
        current_best_index = np.argmin(self.__population_fitness)
        return self.__population[current_best_index], self.__population_fitness[current_best_index]

    def __evaluate(self):
        self.__population_fitness = np.array(
            [_evaluate_specimen_fitness(specimen, self.__flow_matrix, self.__distance_matrix) for specimen in
             self.__population])

    def __selection(self):
        self.__population = self.__selection_method()

    def __tournament_selection(self):
        selected_population = []
        for i in range(0, self.__pop_size):
            competitors_indices = np.random.choice(self.__pop_indices_array, self.__tour, False)
            best_competitor_index = competitors_indices[np.argmin(self.__population_fitness[competitors_indices])]
            selected_population.append(self.__population[best_competitor_index])
        return np.array(selected_population)

    def __roulette_selection(self):
        pop_worst_fitness = np.amax(self.__population_fitness)
        normalized_fitness = [pop_worst_fitness + 1 - self.__population_fitness[i] for i in range(self.__pop_size)]
        fitness_sum = np.sum(normalized_fitness)
        probability_array = [(normalized_fitness[i] / fitness_sum) for i in range(self.__pop_size)]
        selected_indices = np.array(
            np.random.choice(self.__pop_indices_array, size=self.__pop_size, replace=True,
                             p=probability_array))
        return np.array(self.__population[selected_indices])

    def __crossover(self):
        children = []
        for i in range(0, self.__pop_size, 2):
            first_parent_index = np.random.randint(0, self.__pop_size)
            second_parent_index = np.random.randint(0, self.__pop_size)
            first_child, second_child = self.__specimens_crossover(self.__population[first_parent_index],
                                                                   self.__population[second_parent_index])
            children.extend([first_child, second_child])
        self.__population = np.array(children[:self.__pop_size])

    def __specimens_crossover(self, first_parent, second_parent):
        if np.random.randint(0, 1) >= self.__crossover_probability:
            return first_parent, second_parent

        cross_point = np.random.randint(0, len(first_parent))

        first_child = np.append(first_parent[:cross_point], second_parent[cross_point:])
        self.__validate_and_fix_specimen(first_child)

        second_child = np.append(second_parent[:cross_point], first_parent[cross_point:])
        self.__validate_and_fix_specimen(second_child)

        return first_child, second_child

    def __validate_and_fix_specimen(self, specimen):
        if len(specimen) == len(set(specimen)):
            return
        not_found = list(range(1, len(specimen) + 1))
        duplicates_indices = []
        for facility in range(len(specimen)):
            if specimen[facility] not in not_found:
                duplicates_indices.append(facility)
                continue
            not_found.remove(specimen[facility])
        for i in duplicates_indices:
            specimen[i] = not_found[0]
            del not_found[0]

    def __mutation(self):
        specimen_len = self.__num_of_locations
        for specimen in self.__population:
            for location in range(specimen_len):
                if np.random.random() < self.__mutation_probability:
                    swap_location = (location + np.random.randint(1, specimen_len)) % specimen_len
                    temp = specimen[location]
                    specimen[location] = specimen[swap_location]
                    specimen[swap_location] = temp
