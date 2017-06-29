import numpy as np
from selection.evo_alg import *
from selection.selection_problem import SelectionProblem

#Soft constraints
#Percentage lines selected
percentage_weight = 1
#propertion between laura and sarah files
proportion_weight = 1
#How uniform the files are distributed over time
uniformity_weight = 1
#Percentage of lines first checked
first_check_weight =  1
#Percentage of lines checked for a second time
second_check_weight = 1

#Hard constraints
#How many lines max need to be checked (np.inf is also allowed)
max_lines_to_check = 10000
#minimum and maximum percentage of files included
min_percentage_files = 10
max_percentage_files = 20


#Algorithm parameters
number_of_generations = 10000
size_of_generation = 100
#The number of solutions selected to generate the a new generation of solutions with
n_best = 10



weights = [
    percentage_weight,
    proportion_weight,
    uniformity_weight,
    first_check_weight,
    second_check_weight
]

p = SelectionProblem("selection/info.txt", weights, min_percentage_files, max_percentage_files, max_lines_to_check)

solution = get_solution(p, number_of_generations, size_of_generation, n_best)
solution = SelectionProblem.sort_solution_name(solution)
print(p.print_file_names(solution))
p.print_summary(solution)
