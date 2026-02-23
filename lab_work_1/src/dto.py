
class DTO:
    def __init__(self,
                 low_bound: float,
                 up_bound: float,
                 a_param: int,
                 density: int):
        self.low_bound: float = low_bound
        self.up_bound: float = up_bound
        self.a_param: int = a_param
        self.density: int = density
    
    def get_list_params(self, in_frame: bool = True) -> list[str]:
        frame = '#' * 50
        res = [frame] if in_frame else []
        res += [
            f'Модуль расстояния XY: {self.up_bound}',
            f'Параметр А: {self.a_param}',
            f'Плотность заполнения: {self.density}'
        ]
        if in_frame: res.append(frame)
        return res

class GeneticAlgorithmDTO(DTO):
    def __init__(self,
                 low_bound: float,
                 up_bound: float,
                 a_param: int,
                 density: int,
                 population_size: int,
                 n_generations: int,
                 cx_prob: float,
                 mut_prob: float,
                 n_dimension: int,
                 mate_eta: float,
                 mutate_eta: float,
                 mutate_indpb: float,
                 tournsize: int):
        super().__init__(low_bound, up_bound, a_param, density)
        self.population_size: int = population_size
        self.n_generations: int = n_generations
        self.cx_prob: float = cx_prob
        self.mut_prob: float = mut_prob
        self.n_dimension: int = n_dimension
        self.mate_eta: float = mate_eta
        self.mutate_eta: float = mutate_eta
        self.mutate_indpb: float = mutate_indpb
        self.tournsize: int = tournsize

    def get_list_params(self, in_frame: bool = True):
        frame = '#' * 50
        res = [frame] if in_frame else []
        res += super().get_list_params(in_frame=False)
        res += [
            'Метод оптимизации: Генетический алгоритм',
            f'Размер популяции: {self.population_size}',
            f'Количество поколений: {self.n_generations}',
            f'Вероятность скрещивания: {self.cx_prob}',
            f'ETA скрещивания: {self.mate_eta}',
            f'Вероятность мутации: {self.mut_prob}',
            f'INDPB мутации: {self.mutate_indpb}',
            f'ETA мутации: {self.mutate_eta}',
            f'Размер турнира: {self.tournsize}'
        ]
        if in_frame: res.append(frame)
        return res
