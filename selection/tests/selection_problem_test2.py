

import unittest
from ..evo_alg import *
from ..selection_problem import SelectionProblem
from ..selection_data import SelectionData
from ..file_parser import *

class TestOneMaxProblem(unittest.TestCase):
    def test_get_solution(self):
        p = SelectionProblem("selection/info.txt")
        solution = get_solution(p, 500, 100, 10)
        print(solution)
        self.print_solution_statistics(p, solution)


    def print_solution_statistics(self, p, solution):
        percentage = p.get_percentage_score(solution)
        print("Percentage: ")
        print(percentage)
        print("Uniformity: ")
        print(p.get_uniformity_score(solution))
        print("Proportion: ")
        print(p.get_proportion_score(solution))
        print("First check: ")
        print(p.get_first_check_score(solution))
        print("Second check: ")
        print(p.get_second_check_score(solution))
