"""
    This file batch canonicalizes the given files in the folders
    All the files that get an error will be put into a filelist. The filelist are sorted on type of error.
"""

import sys
import os
import subprocess
from shutil import copyfile
from canonicalize.batch_canonicalize_functions import *



directory = sys.argv[1]
result_directory = sys.argv[2]

cwd = os.getcwd()


found_errors = find_errors(directory)



print("Done with errors")
print("writing results")
# For each found error: put the file in a file list and copy files
count = 0
for (k,ref_error) in found_errors.items():
    #Make the folder that contains the errors
    folder = str(count)
    count += 1
    dest = os.path.join(result_directory, folder)
    if not os.path.isdir(dest):
        os.makedirs(dest)
    i = 0
    fl_count = 0
    file_name = "{}/flist_{}.fl".format(dest, fl_count)
    error_file_name = "{}/errors_{}.txt".format(dest, fl_count)
    file = open(file_name, 'w')
    error_file = open(error_file_name, "w")
    file.write("flist_{}\n".format(fl_count))
    for (file_ref, error) in ref_error:
        if i > 100:
            fl_count +=1
            i = 0
            file.close()
            error_file.close()
            file_name = "{}/flist{}.fl".format(dest, fl_count)
            file = open(file_name, 'w')
            error_file_name = "{}/error{}.fl".format(dest, fl_count)
            error_file = open(error_file_name, "w")
        #Add each file to a file_list and add the error to a txt
        i+= 1
        file_name = os.path.basename(file_ref)
        #Copy the file and put file in filelist
        new_file = os.path.join(dest, file_name)
        copyfile(file_ref, new_file)
        file.write("{}\n".format(file_name))
        error_file.write("{} - {}".format(file_name, error))
    file.close()
    error_file.close()




