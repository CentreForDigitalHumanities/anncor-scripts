from numpy import array

from selection.evo_alg import *
from selection.perceptron.perceptron import Perceptron
from selection.selection_problem import SelectionProblem

p = SelectionProblem("selection/info.txt")

perceptron = Perceptron(5)


starting_data = [
    (array([0.9, 0.1,0.1,0.1, 0.1]), 1),
    (array([0.36, 0.1,0.1,0.1, 0.1]), 0),
    (array([0.26, 0.1,0.1,0.1, 0.1]), 0)
]

user_input = ""

perceptron.addData(starting_data)
#perceptron.train(100)

""""
while user_input != "s":
    p.setWeights(perceptron.weights[:-1])
    solution = get_solution(p, 100, 100, 10)
    print(p.printSummary(solution))
    print("Good (1) or bad (0)?")
    user_input = input()
    print(user_input)
    perceptron.addData([(array(p.weights), int(user_input))])
    perceptron.train(100)
    print(perceptron.weights)
"""""

"""""
for i in range(1000):
    p.setWeights(perceptron.weights[:-1])
    solution = get_solution(p, 250, 100, 10)
    ps = p.get_percentage_score(solution)
    print(ps)
    cat = 0
    if ps > 10:
        cat = 0
    else:
        cat = 1
    #print("ff:")
    #print(p.fitness_function(solution))


    perceptron.addData([(array(p.get_score(solution)), cat)])
    #print(perceptron.data)
    perceptron.train(100)
    print("Weights: ")
    print(perceptron.weights)
"""""

solution = get_solution(p, 500, 100, 10)
print(p.printSummary(solution))



