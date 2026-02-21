
class DTO:
    def __init__(self,
                 low_bound: float,
                 up_bound: float,
                 density: int,
                 function: object):
        self.low_bound: float = low_bound
        self.up_bound: float = up_bound
        self.density: int = density
        self.function: object = function

class GeneticAlgorithmDTO(DTO):
    def __init__(self,
                 low_bound: float,
                 up_bound: float,
                 density: int,
                 function: object,
                 population_size: int,
                 n_generations: int,
                 cx_prob: float,
                 mut_prob: float,
                 n_dimension: int,
                 mate_eta: float,
                 mutate_eta: float,
                 mutate_indpb: float,
                 tournsize: int):
        super().__init__(low_bound, up_bound, density, function)
        self.population_size: int = population_size
        self.n_generations: int = n_generations
        self.cx_prob: float = cx_prob
        self.mut_prob: float = mut_prob
        self.n_dimension: int = n_dimension
        self.mate_eta: float = mate_eta
        self.mutate_eta: float = mutate_eta
        self.mutate_indpb: float = mutate_indpb
        self.tournsize: int = tournsize
