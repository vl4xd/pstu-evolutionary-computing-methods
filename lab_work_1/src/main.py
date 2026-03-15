# import numpy as np
import sys
from PyQt5 import QtWidgets

from app.main_window import MainWindow
# from functions import rastrigin
# from genetic_algorithm import GeneticAlgorithm

# XY_MIN = -5.12
# XY_MAX = 5.12

# x = np.linspace(XY_MIN, XY_MAX, 100)
# y = np.linspace(XY_MIN, XY_MAX, 100)
# XX, YY = np.meshgrid(x, y)
# Z = rastrigin(XX, YY)

# ga = GeneticAlgorithm(10, 10, 0.1, 0.1, XY_MIN, XY_MAX, 2, rastrigin)
# ga.optimise(0.1, 0.1, 0.1, 100)

# print(ga.history_pop)

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
    