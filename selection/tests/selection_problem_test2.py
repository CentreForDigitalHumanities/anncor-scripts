

import unittest

from ..evo_alg import *
from ..file_parser import *
from ..selection_problem import SelectionProblem


class testSelectionProblem(unittest.TestCase):
    def test_get_solution(self):
        p = SelectionProblem("selection/info.txt")
        solution = get_solution(p, 100, 100, 10)
        s= sorted(solution,  key = lambda e: e["time_stamp"])
        print([e["name"] for e in s])
        self.print_solution_statistics(p, solution)


    def print_solution_statistics(self, p, solution):
        print("lines to check second time: ")
        print(get_lines_to_check_second(solution))
        print("lines to check first time: ")
        print(get_lines_to_check_first(solution))
        laura_summary = get_summary_of_name(solution, "laura")
        sarah_summary = get_summary_of_name(solution, "sarah")
        print("Laura: ")
        self.print_summary(laura_summary)
        print("Sarah: ")
        self.print_summary(sarah_summary)


    def print_summary(self, summary):
        print("files: ")
        print(summary["nr_of_files"])
        print("lines: ")
        print(summary["nr_of_lines"])
        print("dates: ")
        print(summary["dates"])