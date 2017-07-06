from selection.experiment import *
from selection.selection_problem import SelectionProblem


experiments = [
    Constraints(
        weights={
            'percentage_of_lines_checked': 1,
            'proportion_laura_sarah': 1,
            'uniformity_over_time': 1,
            'lines_checked_first_time': 1,
            'lines_checked_second_time': 1,
        },
        constraints={
            "max_lines_to_check": 75000,
            "min_percentage_files": 10,
            "max_percentage_files": 20,
        }),
    Constraints(
        weights={
            'percentage_of_lines_checked': 1,
            'proportion_laura_sarah': 1,
            'uniformity_over_time': 1,
            'lines_checked_first_time': 1,
            'lines_checked_second_time': 1,
        },
        constraints={
            "max_lines_to_check": 75000,
            "min_percentage_files": 10,
            "max_percentage_files": 20,
        }),
    Constraints(
        weights={
            'percentage_of_lines_checked': 2,
            'proportion_laura_sarah': 3,
            'uniformity_over_time': 1,
            'lines_checked_first_time': 5,
            'lines_checked_second_time': 1,
        },
        constraints={
            "max_lines_to_check": 500,
            "min_percentage_files": 10,
            "max_percentage_files": 20,
        })
]


number_of_iterations = 200
size_of_generation = 100
n_best = 10

info_path = "selection/info.txt"
p = SelectionProblem(info_path)

weights_list = [experiment.weights_to_list() for experiment in experiments]
hard_constraints_list = [experiment.constraints for experiment in experiments]

results = experiment(p, weights_list, hard_constraints_list, number_of_iterations, size_of_generation, n_best, "results.txt")