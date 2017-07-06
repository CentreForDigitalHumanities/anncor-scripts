import numpy as np
from selection.evo_alg import *
from selection.selection_problem import SelectionProblem
import json



def experiment(p, weights_list, hard_constraints_list, number_of_iterations, size_of_generation, n_best, save_location=""):
    if len(weights_list) != len(hard_constraints_list):
        raise ValueError("lenghts of weights_list and hard_constraints do not match: {} != {}". format(len(weights_list), len(hard_constraints_list)))
    solutions = []
    for i in range(len(weights_list)):
        p.weights = weights_list[i]
        p.min_percentage_files = hard_constraints_list[i]["min_percentage_files"]
        p.max_percentage_files = hard_constraints_list[i]["max_percentage_files"]
        p.max_lines_to_check = hard_constraints_list[i]["max_lines_to_check"]
        solution = get_solution(p, number_of_iterations, size_of_generation, n_best)
        solutions.append(solution)
        if(save_location != ""):
            save(p, solution, save_location)
    return solutions


#File to save the solutions to
def save(p, solution, location):
    sorted_solution = p.sort_solution_name(solution)
    with open(location, "a") as f:
        f.write("-"*10)
        f.write("\n")
        names = [e["name"] for e in sorted_solution]
        f.write(str(names))
        f.write("\n")
        f.write("Parameters Settings: \n")
        f.write(p.to_string())
        f.write("\n")
        f.write(p.get_summary(solution))
        f.write("\n")


class Constraints:
    def  __init__(self, weights=[], constraints={}):
        self.weights = weights
        self.constraints = constraints

    def weights_to_list(self):
        return [
            self.weights['percentage_of_lines_checked'],
            self.weights['proportion_laura_sarah'],
            self.weights['uniformity_over_time'],
            self.weights['lines_checked_first_time'],
            self.weights['lines_checked_second_time']
        ]





