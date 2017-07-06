

import unittest
from ..evo_alg import *
from ..one_max_problem import OneMaxProblem



class TestOneMaxProblem(unittest.TestCase):

    def setUp(self):
        self.P = OneMaxProblem()
    def test_get_solution(self):
        solution = self.P.get_random_solution()
        print(solution)

    def test_fitness(self):
        solution = self.P.get_random_solution()
        print(solution)
        print(self.P.fitness_function(solution))

    def test_mate(self):
        sol1 = self.P.get_random_solution()
        sol2 = self.P.get_random_solution()
        sol3 = self.P.mate(sol1, sol2)
        self.assertEqual(len(sol3), 100)

    def test_get_random_solutions(self):
        solutions = self.P.get_random_solutions(200)
        self.assertEqual(len(solutions), 200)

    def test_get_solution(self):
        solution = get_solution(self.P, 1, 1, 1)

        print(solution)
        print(self.P.fitness_function(solution))



