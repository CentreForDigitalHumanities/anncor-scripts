"""
    This script renames the file in proper format, that is, it start the counting at 0 instead of 1
"""


import sys
from shutil import copyfile
import os

input_location = sys.argv[1]
output_location = sys.argv[2]
from utils.textmanipulation import *
def create_new_name(name):
    """
    Returns a new name based on the given name
    :param name:
    :return:
    """
    parts = name.split("_")
    parts = parts[:-1] + parts[2].split(".")
    parts[2] = str(int("".join(list(filter(str.isdigit, parts[2])))) -1)
    parts[2] = "u{}".format(prepend_zeros( 11, parts[2],))
    return "{}_{}_{}.{}".format(*parts)


for root, dirs, files in os.walk(input_location):
    for file in files:
        print(file)
        if "VanKampen" in file:
            new_name = create_new_name(file)
            old_file = os.path.join(root, file)
            new_file = "{}/{}".format(output_location, new_name)
            copyfile(old_file, new_file)


