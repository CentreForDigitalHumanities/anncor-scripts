from file_parser import *
import os
from .evo_alg import *

from .selection_problem import SelectionProblem

p  = SelectionProblem("selection/info.txt")

solution = get_solution(p, 500, 100, 10)
print(solution)