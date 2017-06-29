import unittest
from random import choice
from numpy import array, dot, random
from ..perceptron.perceptron import Perceptron


class TestPerceptron(unittest.TestCase):

    def test_perceptron(self):
        training_data = [(array([0, 0]), 0), (array([0, 1]), 1), (array([1, 0]), 1), (array([1, 1]), 1), ]
        perceptron = Perceptron(2)
        perceptron.addData(training_data)
        perceptron.train(100)
        results = [perceptron.getPrediction(e) for e in [[0,0], [0,1], [1,0], [1,0]]]
        self.assertEqual(results, [0,1,1,1])

    def test_perceptron2(self):
        training_data = [(array([2, 2]), 0), (array([10, 12]), 1), (array([0, 20]), 1), (array([15, 0]), 0), ]
        perceptron = Perceptron(2)
        perceptron.addData(training_data)
        perceptron.train(10000)
        results = [perceptron.getPrediction(e) for e in [[0, 0], [10, 10], [16, 100], [17, 0]]]
        self.assertEqual(results, [0, 0, 1, 0])