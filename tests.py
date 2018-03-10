import unittest
from genetic_algorithm import *
from data_reader import *
import os


class TestClass(unittest.TestCase):
    pop_size = 100
    gen = 100
    Px = 0.7
    Pm = 0.01
    Tour = 5

    def test_evaluate_specimen_fitness_had12(self):
        reader = DataReader()
        path = self.__get_path(r"data/had12.dat")
        n, flow_matrix, distance_matrix = reader.read_data(path)

        genetic_algorithm = GeneticAlgorithm(n, flow_matrix, distance_matrix)
        result = genetic_algorithm.__evaluate_specimen_fitness([3, 10, 11, 2, 12, 5, 6, 7, 8, 1, 4, 9])

        assert result == 1652

    def test_evaluate_specimen_fitness_had14(self):
        reader = DataReader()
        path = self.__get_path(r"data/had14.dat")
        n, flow_matrix, distance_matrix = reader.read_data(path)

        genetic_algorithm = GeneticAlgorithm(n, flow_matrix, distance_matrix)

        assert genetic_algorithm.__evaluate_specimen_fitness([8, 13, 10, 5, 12, 11, 2, 14, 3, 6, 7, 1, 9, 4]) == 2724

    def test_evaluate_specimen_fitness_had16(self):
        reader = DataReader()
        path = self.__get_path(r"data/had16.dat")
        n, flow_matrix, distance_matrix = reader.read_data(path)

        genetic_algorithm = GeneticAlgorithm(n, flow_matrix, distance_matrix)

        assert genetic_algorithm.__evaluate_specimen_fitness(
            [9, 4, 16, 1, 7, 8, 6, 14, 15, 11, 12, 10, 5, 3, 2, 13]) == 3720

    def test_evaluate_specimen_fitness_had18(self):
        reader = DataReader()
        path = self.__get_path(r"data/had18.dat")
        n, flow_matrix, distance_matrix = reader.read_data(path)

        genetic_algorithm = GeneticAlgorithm(n, flow_matrix, distance_matrix)

        assert genetic_algorithm.__evaluate_specimen_fitness(
            [8, 15, 16, 6, 7, 18, 14, 11, 1, 10, 12, 5, 3, 13, 2, 17, 9, 4]) == 5358

    def test_evaluate_specimen_fitness_had20(self):
        reader = DataReader()
        path = self.__get_path(r"data/had20.dat")
        n, flow_matrix, distance_matrix = reader.read_data(path)

        genetic_algorithm = GeneticAlgorithm(n, flow_matrix, distance_matrix)

        assert genetic_algorithm.__evaluate_specimen_fitness(
            [8, 15, 16, 14, 19, 6, 7, 17, 1, 12, 10, 11, 5, 20, 2, 3, 4, 9, 18, 13]) == 6922

    def __get_path(self, file):
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), file)

    @unittest.skip
    def test_validate_and_fix_specimen(self):
        reader = DataReader()
        path = self.__get_path(r"data/had12.dat")
        n, flow_matrix, distance_matrix = reader.read_data(path)
        specimen = [3, 3, 11, 2, 12, 5, 6, 7, 8, 1, 4, 9]

        genetic_algorithm = GeneticAlgorithm(n, flow_matrix, distance_matrix)
        genetic_algorithm.validate_and_fix_specimen(specimen)

        print(specimen)
        assert len(specimen) == len(set(specimen))

if __name__ == '__main__':
    unittest.main()
