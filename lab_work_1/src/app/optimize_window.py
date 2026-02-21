from PyQt5 import QtWidgets, QtGui, QtWebEngineWidgets
from PyQt5.QtCore import QThread, pyqtSignal

from interface.optimize_window import Ui_MainWindow
from genetic_algorithm import GeneticAlgorithm
from dto import DTO, GeneticAlgorithmDTO
from visualizations import Contour


class OptimizeWindow(QtWidgets.QMainWindow):
    def __init__(self, dto: DTO):
        super(OptimizeWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.browser_contour = QtWebEngineWidgets.QWebEngineView()
        self.ui.verticalLayout_contour.addWidget(self.browser_contour)
        self.contour = Contour(dto.low_bound, dto.up_bound, dto.density, dto.function)

        self.browser_3d = QtWebEngineWidgets.QWebEngineView()
        self.ui.verticalLayout_3d.addWidget(self.browser_3d)
        self.browser_metrics = QtWebEngineWidgets.QWebEngineView()
        self.ui.verticalLayout_metrics.addWidget(self.browser_metrics)

        # Начальное обновление браузера
        self._update_browser()

    def _update_browser(self):
        """Обновляет HTML в браузере по текущей фигуре"""
        self.browser_contour.setHtml(self.contour.fig.to_html(include_plotlyjs='cdn'))
