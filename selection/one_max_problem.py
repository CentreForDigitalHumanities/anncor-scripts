import numpy as np
from .evo_alg import Problem


class OneMaxProblem(Problem):
    def get_random_solution(self):
        return np.random.choice([0, 1], size=(100,))

    def fitness_function(self, solution):
        return sum(solution)

    def mate(self, sol1, sol2):
        newSol = []
        for n in range(len(sol1)):
            newSol.append(np.random.choice([sol1[n], sol2[n]]))
        return newSol