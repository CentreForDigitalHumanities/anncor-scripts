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
