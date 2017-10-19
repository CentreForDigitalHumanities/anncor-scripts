"""
    This file is used to generate a selection, it expects two arguments: the percentage of lines to select from each file
    and the location that the results should be stored, this should be a txt file
"""
from selection.parser.file_parser import *
from selection.window import *

import sys

# Arguments needed to generate the selection
percentage = float(sys.argv[1])
# Path to the file where the results should be stored
result_location = sys.argv[2]
# Ref to the folders containing the cha files
cha_files = "./selection/data/cha_files"
# Ref to the folder containing the files that have been looked at for the first time
first_round = "./selection/data/first_round"
# Ref to the folder containing the files that have been looked at for the second time
second_round = "./selection/data/second_round"

line_scores = get_line_score(cha_files, first_round, second_round)
laura_43 = [line_score for line_score in line_scores if line_score[0] == "laura43"]
selection = get_file_selection(line_scores, percentage)
laura_43 = [line_score for line_score in selection if line_score[0] == "laura43"]

total_score_files = [sum([score[1] for score in file[1]]) for file in line_scores]
print(len(total_score_files))
total_score_files = sorted(total_score_files, reverse=True)
print(len(list(filter(lambda x: x > 0, total_score_files))))

def get_nr_to_check(selection, line_scores):
    """
    Gets the number of checks the annotators should do given a selection and a line_score
    :param selection: selection of the lines to check
    :param line_scores: the lines with the given score
    :return: the number of checks that still need to be performed
    """
    total_checks = 0
    maximum_checks = 0
    for (name, lines), (name2, (lines_with_score)) in zip(selection, line_scores):
        score = sum([score for (line, score) in lines_with_score if line in lines])
        max_score = len(lines) * 2
        total_checks += score
        maximum_checks += max_score
    return maximum_checks - total_checks

def get_zero_checked(selection, scores):
    result = []
    for (name, lines), (name2, line_scores) in zip(selection, scores):
        zero_checked = [line for (line, score) in line_scores if line in lines and score==0]
        result.append((name, zero_checked))
    return result

def get_checked(selection, scores):
    result = []
    for (name, lines), (name2, line_scores) in zip(selection, scores):
        zero_checked = [line for (line, score) in line_scores if line in lines and score!=0]
        result += zero_checked
    return result


zero_checked = get_zero_checked(selection, line_scores)
print("Zero times checked: {}".format(len(zero_checked)))
print("checked: {}".format(len(get_checked(selection, line_scores))))
print(selection[0])
print(zero_checked)
# Sorting the selection for convenience
selection = sorted(zero_checked, key=lambda name_lines: name_lines[0])

# Storing the names of the files the names to a file
file_names = []
for (name, lines) in selection:
    file_names = file_names + ["VanKampen_{}_u{}.xml".format(name, prepend_zeros(11, str(line))) for line in lines]

with open(result_location, "w") as f:
    for file_name in file_names:
        f.write("{}\n".format(file_name))
