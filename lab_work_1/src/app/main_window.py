from PyQt5 import QtWidgets, QtGui

from interface.main_window import Ui_MainWindow
from app.optimize_window import OptimizeWindow
from dto import GeneticAlgorithmDTO
from functions import rastrigin


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Заполняем список доступных методов оптимизации
        self.ui.comboBox_method.addItems(['Генетический алогоритм'])
        self.ui.comboBox_method.currentIndexChanged.connect(self.on_model_changed)
        # Обрабатываем видимость полей для текущего алгоритма
        self.on_model_changed()

        # Устанавливаем обработчик событий (нажатие) кнопки "Запустить"
        self.ui.pushButton_start.clicked.connect(self.open_optimize_window)
        self.optimize_windows = []

    def on_model_changed(self):
        idx_method = self.ui.comboBox_method.currentIndex()
        match idx_method:
            case 0:
                # Генетический алогоритм
                self.ui.frame_genetic_params.setVisible(True)

    def open_optimize_window(self):
        idx_method = self.ui.comboBox_method.currentIndex()
        match idx_method:
            case 0:
                # Генетический алогоритм
                dto = GeneticAlgorithmDTO(
                    low_bound = self.ui.doubleSpinBox_xy.value(),
                    up_bound = self.ui.doubleSpinBox_xy.value() * (-1),
                    density = self.ui.spinBox_density.value(),
                    population_size = self.ui.spinBox_population_size.value(),
                    n_generations = self.ui.spinBox_n_generations.value(),
                    cx_prob = self.ui.doubleSpinBox_cx_prob.value(),
                    mut_prob = self.ui.doubleSpinBox_mut_prob.value(),
                    n_dimension = 2,
                    function = rastrigin,
                    mate_eta = self.ui.doubleSpinBox_mate_eta.value(),
                    mutate_eta = self.ui.doubleSpinBox_mutate_eta.value(),
                    mutate_indpb = self.ui.doubleSpinBox_mutate_indpb.value(),
                    tournsize = self.ui.spinBox_tournsize.value()
                )
        new_optimize_window = OptimizeWindow(dto)
        self.optimize_windows.append(new_optimize_window)
        new_optimize_window.show()