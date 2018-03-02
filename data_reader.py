import numpy as np


class DataReader:
    def __init__(self):
        pass

    def read_data(self, file_name):
        file = open(file_name, 'r')
        instance_size = int(file.readline())
        flow_matrix = np.zeros(shape=(instance_size, instance_size))
        distance_matrix = np.zeros(shape=(instance_size, instance_size))
        file.readline()

        for i in range(0, instance_size):
            data_line = [int(data) for data in file.readline().split()]
            flow_matrix[i] = data_line

        file.readline()
        for i in range(0, instance_size):
            data_line = [int(data) for data in file.readline().split()]
            distance_matrix[i] = data_line

        return instance_size, flow_matrix, distance_matrix




