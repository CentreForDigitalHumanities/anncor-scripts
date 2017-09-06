

import unittest

from selection.selection_problem_example.selection_data import SelectionData
from ..evo_alg import *
from ..selection_problem_example.selection_problem_example import SelectionProblem


class TestOneMaxProblem(unittest.TestCase):
    def setUp(self):
        self.data = {}
        for y in range(1, 6):
            self.data[y] = {}
            for m in range(1, 13):
                if m == 6:
                    self.data[y][m] = {
                        "n_files": 100,
                        "n_annotated": 100
                    }
                else:
                    self.data[y][m] = {
                        "n_files": 10,
                        "n_annotated": 0
                    }
        self.selectionData = SelectionData(self.data)
        self.p = SelectionProblem(self.selectionData)

    def test_get_random_solution(self):
        solution = self.p.get_random_solution()
        self.assertEqual(len(solution), 5)

    def test_mate_function(self):
        sol1 = self.p.get_random_solution()
        sol2 = self.p.get_random_solution()
        sol3 = self.p.mate(sol1, sol2)

    def test_get_solution(self):
        pass
        #print("get solution")
        #solution = get_solution(self.p, 100, 100, 10)
        #print(solution)
        #self.assertEqual(self.p.fitness_function(solution), 1)
