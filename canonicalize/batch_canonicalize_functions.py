import sys
import os
import subprocess
from shutil import copyfile


list_of_errors = [
    'no source node for index',
    "leaf node without @begin",
    "no target node for index",
    "without @pos",
    "line",
    "is used more than once",
    "leaf node without @root",
    "sorting",
    "mismatched tag"
]


def get_error_out_of_lines(lines):
    # Get the error out of the file
    error = None
    step_1 = None
    i = 0
    for line in lines:
        if "Exception" in line or "Error" in line or "error" in line or "mismatched tag" in line:
            print(line)
            break
        i += 1


    try:
        error = lines[i]
    except IndexError as e:
        print(step_1)
        print(e)
        print(lines)
        raise Exception("Not able to parse lines")
    return error

def canonicalize_one_file(file_ref, found_errors):
    """
    Canonicalizes one file with the given file_ref, updates the found errors if we find an error
    :param file_ref
    """

    cwd = os.getcwd()
    script = os.path.join(cwd, "canonicalize/dtcanonicalize.py")

    with open("./temp_errors.txt", "w"):
        pass
    # Open the file to read to
    with open("./temp_errors.txt", "r+") as output:
        subprocess.call("python {} '{}'".format(script, file_ref), shell=True, stderr=output)
        output.seek(0)
        lines = output.readlines()

        # If there are lines in de txt than there was a fail
        if lines != []:

            error = get_error_out_of_lines(lines)
            error_found = False
            # Put the file in the found errors under the right error
            for know_error in list_of_errors:
                if know_error in error:
                    found_errors[know_error].append((file_ref, error))
                    error_found = True
                    break
            # Do this if we found an error that we have not found before
            if not error_found:
                raise ValueError("error not in list of common errors: {}".format(error))

    os.remove("./temp_errors.txt")





def find_errors(directory, remove=True):
    """
    Runs the dtcanonicalize for every vankampen file in the given directory and subdirectories
    :param directory: The directory to search in
    :return: An array full of tuples (file_ref, error)
    """


    # Dictionary with the errors we found, sorted by error
    found_errors = {

    }

    if not os.path.isdir("./parsed_files"):
        os.makedirs("./parsed_files")

    # Add errors we sort on to the dict of found errors
    for error in list_of_errors:
        found_errors[error] = []

    for root, dirs, files in os.walk(directory):
        for name in files:
            # Only use the vankampen xml files
            if "VanKampen" in name and ".xml" == name[len(name) - 4:]:

                cwd = os.getcwd()
                file_ref = os.path.join(root, name)

                new_file = os.path.join("./parsed_files", name)
                copyfile(file_ref, new_file)
                canonicalize_one_file(new_file, found_errors)
                if remove:
                    os.remove(file_ref)
    return found_errors
