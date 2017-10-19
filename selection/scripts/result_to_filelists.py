"""
    This script generates filelists based on a given result from the parse,
    It needs three arguments: an input file, a folder containing the xml files and a output location (folder)
"""
import sys
from utils.textmanipulation import *
import os
from shutil import copyfile

input_file = sys.argv[1]
xml_folder = sys.argv[2]
output_location = sys.argv[3]

def find(name, path):
    #print(name)
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)


def get_next_hundered_lines(file):
    """
    Gets the next hundred lines
    :param file:
    :return:
    """
    count = 0
    result = []
    while count < 100:
        count += 1
        next_line = file.readline()
        if next_line != "":
            result.append(next_line)
        else:
            break
    return result


# Here we read the input file and for every hundred lines create a folder with the files and a file list
with open(input_file, "r") as f:
    next_hundred = get_next_hundered_lines(f)
    count = 0
    name = "?"
    while next_hundred != []:
        #Create the folder

        directory = "{}/FL{}".format(output_location, count)
        file_name = "{}/flist_vk{}.fl".format(directory, count)
        count += 1
        if not os.path.exists(directory):
            os.makedirs(directory)

        #Write lines to the filelist
        with open(file_name, "w") as result:
            result.write("Map {} \n".format(prepend_zeros(3, str(count))))
            for line in next_hundred:
                result.write(line)

        for line in next_hundred:
            source = find(line.strip(), xml_folder)
            copyfile(source, "{}/{}".format(directory, line.strip()))
            #Remove the file (is for a speed up)
            os.remove(source)

        next_hundred = get_next_hundered_lines(f)
