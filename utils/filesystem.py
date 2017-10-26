"""
    This file should contain functions that manipulate the filesystem
"""
import os
import zipfile


def unzip(path):
    """
    Unzips a zip folder and creates a folder containing the results
    :param path: The path to the folder to zip
    :return: The new name fo the path
    """
    zip_ref = zipfile.ZipFile(path, 'r')
    new_path = path[:-3]
    zip_ref.extractall(new_path)
    zip_ref.close()
    return new_path


def list_all_files_with_extension(path, extension, do_unzip=True):
    """"
        Lists all the files in the path with the given extension, id do_unzip is true all the zip folders it encounters will be zipped and deleted
        :param path: The path that we list all the files in, this includes the subfolders and zip files
        :param extension: The extension that we look at
        :return:the files in the path with the given extension
        :rtype string[]
    """
    files = []
    for file in os.listdir(path):
        if file.endswith(extension):
            files.append(file)
        if do_unzip and file.endswith(".zip"):
            new_path = unzip(os.path.join(path, file))
            os.remove(os.path.join(path, file))
            files = files + list_all_files_with_extension(new_path, extension)
        # Dive into subfolders.
        if os.path.isdir(os.path.join(path, file)):
            files = files + list_all_files_with_extension(os.path.join(path, file), extension)
    return files

def list_files(path, criteria=None):
    files = []
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        if os.path.isfile(file_path):
            if criteria:
                if criteria(file_path):
                    files.append(file_path)
            else:
                files.append(file_path)
        if os.path.isdir(file_path):
            files = files + list_files(file_path, criteria)
    return files

def find_duplicates(path, extension):
    """
    Find duplicate files with the same extension
    :param path:
    :param extension:
    :return:
    """
    files = list_all_files_with_extension(path, extension)
    result = set()
    duplicates = set()
    for file in files:
        if file in result:
            duplicates.add(file)
        else:
            result.add(file)
    return duplicates


def list_splited_paths(dir_ref, criteria=None):
    """
        lists all files in the dir_ref that pass the criteria function into splited paths
    :param dir_ref: Reference to the directory to list the files
    :param criteria: a function that returns true if a file needs to be included into the list
    :return:
    """
    files = list_files(dir_ref, criteria)
    return split_paths(files)


def split_paths(paths):
    """
    Splits all the given path into the path to the dest folder and the actual file name
    :param paths:
    :return:
    """
    results = []
    for path in paths:
        results.append(os.path.split(path))
    return results

def sort_splited_paths_on_filename(splited_paths):
    return sorted(splited_paths, key=lambda split_path: split_path[1])

def print_list_to_file(file_ref, list):
    with open(file_ref, "w+") as f:
        for item in list:
            f.write("{}\n".format(item))



