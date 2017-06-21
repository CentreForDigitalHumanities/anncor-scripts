from .evo_alg import *
import numpy as np
from .file_parser import *

class SelectionProblem(Problem):
    def __init__(self, data_path):
        self.selection_data = load_info(data_path)
        self.total_lines = get_total_lines(self.selection_data)
        self.total_files = len(self.selection_data)
        self.proportion = 74/50


    def get_random_solution(self):
        nr_of_files = round((25 * np.random.rand()) + 10) * self.total_files / 100
        solution = np.random.choice(self.selection_data, int(nr_of_files), replace=False)
        return solution

    def mate(self, sol1, sol2):
        sol1s = set([s["name"] for s in sol1])
        sol2s = set([s["name"] for s in sol2])
        sol3s = list(sol1s.union(sol2s))
        sol3 = np.concatenate([sol1, sol2])

        solution = np.random.choice(sol3s, max([len(sol1), len(sol2)]), replace=False)
        result = []
        for s in solution:
            for i in range(0, len(sol3)):
                if sol3[i]["name"] == s:
                    result.append(sol3[i])
                    break
        return result


    def fitness_function(self, solution):
        a= [
            1,
            1,
            1,
            1,
            1
        ]
        score = [
            self.get_percentage_score(solution),
            self.get_proportion_score(solution),
            self.get_uniformity_score(solution),
            self.get_first_check_score(solution),
            self.get_second_check_score(solution)
        ]

        return np.dot(a, score)

    def get_proportion_score(self, solution):
        return 1/(1 + self.proportion_error(solution))

    def get_percentage_score(self, solution):
        return self.get_line_percentage(solution)

    def proportion_error(self, solution):
        proportion = self.get_proportion(solution)
        if proportion == -1:
            return np.inf
        return (self.proportion - proportion)**2

    def get_line_percentage(self, solution):
        nr_lines = get_total_lines(solution)
        return nr_lines/self.total_lines

    def get_uniformity_score(self, solution):
        return self.get_mean_differences(solution)

    def get_mean_differences(self, solution):
        sarah_solution = [e for e in solution if "sarah" in e["name"]]
        laura_solution = [e for e in solution if "laura" in e["name"] ]

        if len(sarah_solution) != 0:
            sarah_mse = self.get_mean_square_error_date_difs(sarah_solution)
        else:
            sarah_mse = -np.inf
        if len(laura_solution) != 0:
            laura_mse = self.get_mean_square_error_date_difs(laura_solution)
        else:
            laura_mse = -np.inf
        return 1 / (1+ laura_mse + sarah_mse)

    def get_date_differences(self, solution):
        difs = []
        for i in range(0, len(solution) - 1):
            difs.append(solution[i + 1]["time_stamp"] - solution[i]["time_stamp"])
        return difs


    def get_mean_square_error_date_difs(self, solution):
        s = sorted(solution , key = lambda e: e["time_stamp"] )
        difs = self.get_date_differences(s)
        if(len(difs) == 0):
            return -np.inf
        mean = sum(difs)/len(difs)
        error = [(d - mean)**2 for d in difs]
        mse = sum(error)
        return mse



    def get_first_check_score(self, solution):
        return get_total_first_checked(solution)/get_total_lines(solution)

    def get_second_check_score(self, solution):
        return get_total_second_checked(solution)/get_total_lines(solution)

    def get_proportion(self, solution):
        laura = sum("laura" in e["name"] for e in solution)
        sarah = sum("sarah" in e["name"] for e in solution)
        if sarah == 0:
            return -1
        else:
            return laura/sarah


