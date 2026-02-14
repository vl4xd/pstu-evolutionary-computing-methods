import numpy as np

def rastrigin(*args, a: float = 10.0) -> float:
    '''
    Docstring for rastrigin

    https://ru.wikipedia.org/wiki/Функция_Растригина
    '''

    n = len(args)
    # coords[0, i, j] равен XX[i, j], а coords[1, i, j] равен YY[i, j]...
    coords = np.array(args)
    # axis=0 - суммируем по строкам (по аргументам)
    return a * n + np.sum(coords**2 - a * np.cos(2 * np.pi * coords), axis=0)