from .evo_alg import *
import numpy as np


class SelectionProblem(Problem):
    def __init__(self, selectionData):
        self.selectionData = selectionData

    def get_random_solution(self):
        solution = []
        for year in self.selectionData.data:
            solution.append(self.selectionData.get_random_from_year(year))
        return solution

    def fitness_function(self, solution):
        sum_annotated = sum([month["n_annotated"] for month in solution])
        sum_n_files = sum([month["n_files"] for month in solution])
        return sum_annotated/sum_n_files

    def mate(self, sol1, sol2):
        new_solution = []
        for i in range(0, len(sol1)):
            new_solution.append(np.random.choice([sol1[i], sol2[i]]))
        return new_solution
