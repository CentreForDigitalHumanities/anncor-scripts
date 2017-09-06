from selection.parser.file_parser import *
from selection.window import *

line_scores = get_line_score("./selection/data/cha_files", "./selection/data/first_round", "./selection/data/second_round")

selection = get_file_selection(line_scores, 0.1)

for i in range(len(line_scores)):
    if line_scores[i][0] == "laura74":
        print(line_scores[i])
        print(selection[i])
