import time
from PyQt5 import QtWidgets, QtWebEngineWidgets
from PyQt5.QtCore import QThread, pyqtSignal

from interface.optimize_window import Ui_MainWindow
from genetic_algorithm import GeneticAlgorithm
from dto import DTO, GeneticAlgorithmDTO
from visualizations import Contour, Metrics

class GeneticAlgorithmThread(QThread):
    # Сигналы для передачи данных из потока в главный поток
    update_signal = pyqtSignal(int, list, list)  # номер поколения, популяция, значения приспособленности
    finished_signal = pyqtSignal()

    def __init__(self, ga, mate_eta, mutate_eta, mutate_indpb, tournsize):
        super().__init__()
        self.ga = ga
        self.mate_eta = mate_eta
        self.mutate_eta = mutate_eta
        self.mutate_indpb = mutate_indpb
        self.tournsize = tournsize
        self._is_running = True

    def run(self):
        # Запускаем генератор оптимизации
        for gen, pop, fits in self.ga.optimise(self.mate_eta, 
                                               self.mutate_eta, 
                                               self.mutate_indpb, 
                                               self.tournsize):
            if not self._is_running:
                break
            self.update_signal.emit(gen, pop, fits)
            time.sleep(0.1)
        self.finished_signal.emit()

    def stop(self):
        self._is_running = False

class OptimizeWindow(QtWidgets.QMainWindow):
    def __init__(self, dto: DTO):
        super(OptimizeWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.dto = dto

        self.browser_contour = QtWebEngineWidgets.QWebEngineView()
        self.ui.verticalLayout_contour.addWidget(self.browser_contour)

        self.browser_metrics = QtWebEngineWidgets.QWebEngineView()
        self.ui.verticalLayout_metrics.addWidget(self.browser_metrics)

        self.history_pop: list = []
        self.history_min: list = []
        self.history_avg: list = []
        self.history_max: list = []

        self.thread = None
        self._start_algorithm_thread()

    def _update_browser(self):
        """Обновляет HTML в браузере по текущей фигуре"""
        metrics = Metrics(self.history_min, self.history_avg, self.history_max)
        self.browser_metrics.setHtml(metrics.fig.to_html(include_plotlyjs='https://cdn.plot.ly/plotly-2.27.0.min.js'))
        # contour = Contour(dto.low_bound, dto.up_bound, dto.a_param, dto.density)
        # self.browser_contour.setHtml(self.contour.fig.to_html(include_plotlyjs='cdn'))

    def _start_algorithm_thread(self):
        if isinstance(self.dto, GeneticAlgorithmDTO):
            self.ui.listWidget_logs.addItems(self.dto.get_list_params())
            ga = GeneticAlgorithm(self.dto.population_size,
                                  self.dto.n_generations,
                                  self.dto.cx_prob,
                                  self.dto.mut_prob,
                                  self.dto.low_bound,
                                  self.dto.up_bound,
                                  self.dto.a_param,
                                  self.dto.n_dimension)
            self.thread = GeneticAlgorithmThread(
                ga,
                self.dto.mate_eta,
                self.dto.mutate_eta,
                self.dto.mutate_indpb,
                self.dto.tournsize
            )
            self.thread.update_signal.connect(self.on_update)
            self.thread.finished_signal.connect(self.on_finished)
            self.thread.start()
            # for gen, pop, fits in ga.optimise(self.dto.mate_eta,
            #                              self.dto.mutate_eta,
            #                              self.dto.mutate_indpb,
            #                              self.dto.tournsize):
            #     best_ind, best_ind_val = GeneticAlgorithm.get_best_from_gen(pop, fits)
            #     self.ui.listWidget_logs.addItem(f'№{gen} | Лучший {best_ind} = {best_ind_val}')
            #     self.metrics.update_points(*GeneticAlgorithm.get_min_avg_max(fits))
            #     self._update_browser()

    def on_update(self, gen, pop, fits):
        # Этот метод выполняется в главном потоке, можно безопасно обновлять GUI
        best_ind, best_val = GeneticAlgorithm.get_best_from_gen(pop, fits)
        self.ui.listWidget_logs.addItem(f'№{gen} | Лучший {best_ind} = {best_val}')
        self.history_pop.append(pop)
        c_min, c_avg, c_max = GeneticAlgorithm.get_min_avg_max(fits)
        self.history_min.append(c_min)
        self.history_avg.append(c_avg)
        self.history_max.append(c_max)

    def on_finished(self):
        # Создать графики после завершения алгоритма
        self._update_browser()
        # self.thread = None

    def closeEvent(self, event):
        """При закрытии окна останавливаем поток, если он ещё работает"""
        if self.thread and self.thread.isRunning():
            pass
            self.thread.stop()
            self.thread.wait()
        event.accept()
