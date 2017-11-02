from utils.xml import *
from utils.filesystem import *


def compare_dirs(dir1, dir2, selection, tags, ignore_characters):
    files_1 = sort_splited_paths_on_filename(split_paths(list_files(dir1, selection)))
    files_2 = sort_splited_paths_on_filename(split_paths(list_files(dir2, selection)))
    return compare_files(files_1, files_2, tags, ignore_characters)


def compare_files(files_1, files_2, tags, ignore_characters):
    """
    Compare the given files. Assumes the files are sorted on the file name.
    :param files_1: list with splitted paths sorted on name
    :param files_2: list with splitted paths sorted on name
    :param tags: tags to compare
    :param ignore_characters: characters to ignore while comparing
    :changes Deletes files out of files_2 when we have no match with files_1 (This to speed up consecutive calls)
    :return:
    """
    print(len(files_1) + len(files_2) , " to go")
    results = []
    #Base cases
    if files_1 == []:
        return []
    elif files_2 == []:
        return []

    # Get the name
    file_1_name = files_1[0][1]
    file_2_name = files_2[0][1]

    # While the file names are not the same
    while file_1_name != file_2_name:
        #If file_1_name is bigger than file_2 name delete file_2
        if file_1_name > file_2_name:
            os.remove(os.path.join(files_2[0][0], files_2[0][1]))
            files_2 = files_2[1:]
            if files_2 == []:
                return []
        else:
            files_1 = files_1[1:]
            if files_1 == []:
                return []
        file_1_name = files_1[0][1]
        file_2_name = files_2[0][1]

    #File names are the same, get the differences
    differences = get_differences(os.path.join(files_1[0][0], files_1[0][1]), os.path.join(files_2[0][0], files_2[0][1]), tags, ignore_characters)
    if differences:
        results.append(create_dict_diff(files_1[0], files_2[0], differences))
    return results + compare_files(
        files_1[1:],
        files_2[1:],
        tags,
        ignore_characters
    )


def create_dict_diff(file_1, file_2, differences):
    return {
        "file": file_1[1],
        "sentence": differences['sentence'],
        "locations": [file_1[0], file_2[0]]
    }

def get_differences(file_ref_1, file_ref_2, tags, ignore_characters):
    differences = {}
    for tag in tags:
        print("tag")
        dif = compare_xml_tag(file_ref_1,
                              file_ref_2, tag, ignore_characters)
        if dif:
            differences[tag] = dif
    return differences
