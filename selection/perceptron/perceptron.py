from random import choice
from numpy import array, dot, random
import numpy as np


class Perceptron:
    def __init__(self, size):
        self.weights = random.rand(size + 1)
        self.data = []
        #make this adjustable
        self.eta = 0.2
        self.errors = []

    def unit_step(self, x):
        return 0 if x < 0 else 1

    def addData(self, data):
        self.data += data

    def train(self, n_sessions):
        for i in range(n_sessions):
            x, expected = choice(self.data)
            x =np.append(x,[1])

            result = dot(self.weights, x)
            #print(x)

            error = expected - self.unit_step(result)
            #print("expected, results, error ")
            #print(expected)
            #print(result)
            #print(error)
            self.errors.append(error)
            self.weights += self.eta * error * x
            #print(self.data)


    def getPrediction(self, input):
        return self.unit_step(dot(self.weights , input + [1]))
