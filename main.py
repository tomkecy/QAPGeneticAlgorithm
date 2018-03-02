from data_reader import *

pop_size = 100
gen = 100
Px = 0.7
Pm = 0.01
Tour = 5

reader = DataReader()
n, A, B = reader.read_data("data/had20.dat")
print(n)
print(A)
print(B)