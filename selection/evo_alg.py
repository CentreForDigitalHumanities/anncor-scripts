import random
from abc import abstractmethod

def getFittest(pop, fitness_function, n):
    return sorted(pop, key=lambda individual: fitness_function(individual), reverse=True)[0:n]

def mate(fittest, mate_function, sizePop):
    new_pop = []
    for n in range(0,sizePop):
        #improvement make selecting the same individual impossible
        new_pop.append(mate_function(random.choice(fittest), random.choice(fittest)))
    return new_pop


def get_solution(P, nGen, sizePop, nBest):
    pop = P.get_random_solutions(sizePop)
    best = None
    for gen in range(0,nGen):
        fittest = getFittest(pop, P.fitness_function, nBest)
        freshPop =P.get_random_solutions(round(0.3 * nBest))
        fittest += freshPop
        pop = mate(fittest, P.mate, sizePop)
        best = fittest[0]
    return best

class Problem:
    @abstractmethod
    def get_random_solution(self):
        pass

    def get_random_solutions(self, n):
        return [self.get_random_solution() for i in range(0, n)]

    @abstractmethod
    def fitness_function(self, solution):
        pass

    @abstractmethod
    def mate(self, sol1, sol2):
        pass








