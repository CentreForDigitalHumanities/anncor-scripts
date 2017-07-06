
import unittest
from ..evo_alg import *



class TestConvert(unittest.TestCase):

    def test_get_fittest(self):
        pop = [1,2,3,4,5,6,7,8,9,10,11,11,12,15]
        def fitnessFunction(individual):
            return individual
        top_5 = [15,12,11,11,10]
        self.assertEqual(getFittest(pop, fitnessFunction, 5), top_5)

    def test_mate(self):
        pop = [1,2,3,4,5,6,7,8,9,10]
        def mate_function(i1, i2):
            return (i1 + i2) /2
        newPop = mate(pop, mate_function, 10)
        print(newPop)


