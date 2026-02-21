import random
import copy
import numpy as np
from deap import base, creator, tools, algorithms


class GeneticAlgorithm:

    def __init__(self,
                 population_size: int,
                 n_generations: int,
                 cx_prob: float,
                 mut_prob: float,
                 low_bound: float,
                 up_bound: float,
                 n_dimension: int,
                 function: object):
        '''
        Docstring for __init__

        :param self: Description
        :param population_size: Description
        :type population_size: int
        :param n_generations: Description
        :type n_generations: int
        :param cx_prob: Description
        :type cx_prob: float
        :param mut_prob: Description
        :type mut_prob: float
        :param low_bound: Description
        :type low_bound: float
        :param up_bound: Description
        :type up_bound: float
        :param n_dimension: Длина хромосом особи: n_dimension=2 ([x1, x2])
        :type n_dimension: int
        :param function: Функция для оптимизации
        :type function: object
        '''

        self.population_size: int = population_size
        self.n_generations: int = n_generations
        self.cx_prob: float = cx_prob
        self.mut_prob: float = mut_prob
        self.low_bound: float = low_bound
        self.up_bound: float = up_bound
        self.n_dimension: int = n_dimension
        self.function = function
        self.history_pop: list = []
        self.history_min: list = []
        self.history_avg: list = []
        self.history_max: list = []
        self.history_nevals: list = []


    def _evaluate(self, individual):
        # individual - [float,...]
        # , - возвращает кортеж
        return self.function(*individual),

    def optimise(self,
                 mate_eta: float,
                 mutate_eta: float,
                 mutate_indpb: float,
                 tournsize: int):
        # Одна цель (одная целевая функция) - кортеж -1.0, (минимизация целевой функции)
        creator.create('FitnessMin', base.Fitness, weights=(-1.0,))
        creator.create('Individual', list, fitness=creator.FitnessMin)
        toolbox = base.Toolbox()
        # Регистрация функции генерации аллеля (значения гена) в промежутке [low_bound, up_bound]
        toolbox.register('attr_float', random.uniform, a=self.low_bound, b=self.up_bound)
        toolbox.register('individual',
                         tools.initRepeat,
                         creator.Individual,
                         toolbox.attr_float,
                         n=self.n_dimension)
        # Генератор популяции: создаёт список особей
        toolbox.register("population", tools.initRepeat, list, toolbox.individual)
        # Регистрация оценки (целевая функция)
        toolbox.register('evaluate', self._evaluate)
        # https://deap.readthedocs.io/en/master/api/tools.html#deap.tools.mutPolynomialBounded
        toolbox.register("mate", tools.cxSimulatedBinaryBounded,
                         low=self.low_bound,
                         up=self.up_bound,
                         eta=mate_eta)
        toolbox.register("mutate",
                         tools.mutPolynomialBounded,
                         low=self.low_bound,
                         up=self.up_bound,
                         eta=mutate_eta,
                         indpb=mutate_indpb)
        toolbox.register("select", tools.selTournament, tournsize=tournsize)
        # Начальная популяция
        pop = toolbox.population(n=self.population_size)
        # Hall of Fame для сохранения лучшей особи за всё время
        hof = tools.HallOfFame(maxsize=1)
        # Статистика
        stats = tools.Statistics(lambda ind: ind.fitness.values)
        stats.register("min", np.min)
        # Запуск эволюции
        # https://deap.readthedocs.io/en/master/api/algo.html#deap.algorithms.eaSimple
        # pop, log = algorithms.eaSimple(pop,
        #                                toolbox,
        #                                cxpb=self.cx_prob,
        #                                mutpb=self.mut_prob,
        #                                ngen=self.n_generations,
        #                                halloffame=hof,
        #                                stats=stats,
        #                                verbose=verbose)
        self.history_nevals.append(len(pop))
        # Оценка начальной популяции
        fitnesses = toolbox.map(toolbox.evaluate, pop)
        for ind, fit in zip(pop, fitnesses):
            ind.fitness.values = fit
        # self.history_pop.append(copy.deepcopy(pop))
        current_fits = [ind.fitness.values[0] for ind in pop]
        # self.history_min.append(np.min(current_fits))
        # self.history_avg.append(np.mean(current_fits))
        # self.history_max.append(np.max(current_fits))
        yield copy.deepcopy(pop), current_fits
        # Цикл по поколениям
        for gen in range(1, self.n_generations + 1):
            # Отбор (создаёт новую популяцию того же размера)
            selected = toolbox.select(pop, len(pop))
            # Клонирование, чтобы не изменять родителей
            offspring = list(map(toolbox.clone, selected))
            # Скрещивание и мутация (varAnd)
            offspring = algorithms.varAnd(offspring, toolbox, self.cx_prob, self.mut_prob)
            # Оценка потомков с невычисленным fitness
            invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
            self.history_nevals.append(invalid_ind)
            fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
            for ind, fit in zip(invalid_ind, fitnesses):
                ind.fitness.values = fit
            # self.history_pop.append(copy.deepcopy(offspring))
            current_fits = [ind.fitness.values[0] for ind in offspring]
            # self.history_min.append(np.min(current_fits))
            # self.history_avg.append(np.mean(current_fits))
            # self.history_max.append(np.max(current_fits))
            yield copy.deepcopy(offspring), current_fits
            # Замена популяции
            pop[:] = offspring
            # Обновление hof
            hof.update(pop)

            # if verbose:
            #     print(f"gen {gen}: min {self.history_min[-1]:}, hof {hof[0]}")
