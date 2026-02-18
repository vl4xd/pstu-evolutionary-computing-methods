import numpy as np

from functions import rastrigin
from genetic_algorithm import GeneticAlgorithm

XY_MIN = -5.12
XY_MAX = 5.12

x = np.linspace(XY_MIN, XY_MAX, 100)
y = np.linspace(XY_MIN, XY_MAX, 100)
XX, YY = np.meshgrid(x, y)
Z = rastrigin(XX, YY)

ga = GeneticAlgorithm(10, 10, 0.1, 0.1, XY_MIN, XY_MAX, 2, rastrigin)
ga.optimise(0.1, 0.1, 0.1, 10, True)

print(ga.history_pop)