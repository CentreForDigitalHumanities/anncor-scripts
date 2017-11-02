""""
It will create filelists and copies the files with the given result file
"""
import sys
from utils.filesystem import *
result_file = sys.argv[1]
result_location = sys.argv[2]



#Pipeline

#Load the info of the files
files_info = read_lines_as_dict(result_file)
print(files_info[0])
files = [os.path.join(i["locations"][1], i["file"]) for i in files_info]

create_filelists(files, result_location)

