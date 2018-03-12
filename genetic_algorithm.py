import numpy as np


class GeneticAlgorithm:
    def __init__(self, num_of_locations, pop_size, flow_matrix, distance_matrix, mutation_probability,
                 crossover_probability, tour, data_logger, selection_method='tournament'):
        self.__num_of_locations = num_of_locations
        self.__flow_matrix = flow_matrix
        self.__distance_matrix = distance_matrix
        self.__pop_size = pop_size
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

    def initialise_population(self):
        self.__population = np.array([self.__generate_specimen() for _ in range(0, self.__pop_size)])

    def __generate_specimen(self):
        specimen = [i for i in range(1, self.__num_of_locations + 1)]
        np.random.shuffle(specimen)
        return specimen

    def run(self, generations):
        current_generation = 1
        self.initialise_population()
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
            self.__data_logger.write_log(current_generation, current_best_fitness, np.average(self.__population_fitness),
                                         np.amax(self.__population_fitness))

            if current_best_fitness < global_best_fitness:
                global_best_fitness = current_best_fitness
                global_best_specimen = current_best_specimen

        return global_best_specimen, global_best_fitness

    def __get_current_best(self):
        current_best_index = np.argmin(self.__population_fitness)
        return self.__population[current_best_index], self.__population_fitness[current_best_index]

    def __evaluate(self):
        self.__population_fitness = np.array([self.__evaluate_specimen_fitness(specimen) for specimen in self.__population])

    def __evaluate_specimen_fitness(self, specimen):
        fitness_acc = 0
        for facility in range(0, len(specimen)):
            for other_facility in range(0, len(specimen)):
                if facility == other_facility:
                    continue
                fitness_acc += self.__flow_matrix[facility, other_facility] * self.__distance_matrix[
                    specimen[facility] - 1,
                    specimen[other_facility] - 1]
        return fitness_acc

    def __selection(self):
        self.__population = self.__selection_method()

    def __tournament_selection(self):
        selected_population = []
        for i in range(0, self.__pop_size):
            competitors_indices = np.random.choice([i for i in range(0, self.__pop_size)], self.__tour, False)
            best_competitor_index = competitors_indices[np.argmin(self.__population_fitness[competitors_indices])]
            selected_population.append(self.__population[best_competitor_index])
        return np.array(selected_population)

    def __roulette_selection(self):
        fitness_sum = np.sum(self.__population_fitness)
        probability_array = [(self.__population_fitness[i]/fitness_sum)*self.__pop_size for i in range(self.__pop_size)]
        alias = [0 for _ in range(0, self.__pop_size)]
        prob = [0 for _ in range(0, self.__pop_size)]
        small = []
        large = []
        selected_population = []

        for i in range(0, self.__pop_size):
            if probability_array[i] < 1:
                small.append(i)
            else:
                large.append(i)
        while small and large:
            l = small.pop(0)
            g = large.pop(0)

            prob[l] = probability_array[l]
            alias[l] = g
            probability_array[g] = (probability_array[g] + probability_array[l]) - 1
            if probability_array[g] < 1:
                small.append(g)
            else:
                large.append(g)
        while large:
            g = large.pop(0)
            prob[g] = 1
        while small:
            l = small.pop(0)
            prob[l] = 1

        #generation
        for _ in range(0, self.__pop_size):
            i = np.random.randint(0, self.__pop_size)
            if np.random.rand() < prob[i]:
                selected_population.append(self.__population[i])
            else:
                selected_population.append(self.__population[alias[i]])
        return np.array(selected_population)

    def __crossover(self):
        children = []
        for i in range(0, self.__pop_size, 2):
            first_parent_index = np.random.randint(0, self.__pop_size)
            second_parent_index = np.random.randint(0, self.__pop_size)
            first_child, second_child = self.__specimens_crossover(self.__population[first_parent_index],
                                                                   self.__population[second_parent_index])
            children.extend([first_child, second_child])
        self.__population = np.array(children)

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
        for facility in range(0, len(specimen)):
            if specimen[facility] not in not_found:
                duplicates_indices.append(facility)
                continue
            not_found.remove(specimen[facility])
        for i in duplicates_indices:
            specimen[i] = not_found[0]
            del not_found[0]

    def __mutation(self):
        for specimen in self.__population:
            if np.random.random() < self.__mutation_probability:
                first_index = np.random.randint(0, len(specimen))
                second_index = (first_index + np.random.randint(1, len(specimen))) % len(specimen)
                temp = specimen[first_index]
                specimen[first_index] = specimen[second_index]
                specimen[second_index] = temp




