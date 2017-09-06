from selection.parser.file_parser import *

def first_check_test(e):
    if(e["nr_of_lines"] < e["first_check"]):
        print("more firsted checked than nr of lines")
        print(e)

def second_check_test(e):
    if (e["nr_of_lines"] < e["second_check"]):
        print("more second checked than nr of lines")
        print(e)

def first_second_test(e):
    if (e["first_check"] < e["second_check"]):
        print("more second checked than first checked")
        print(e)

def totally_checked(e):
    if(e["first_check"] == e["nr_of_lines"]):
        print("first checked")
        print(e)
    if(e["second_check"] == e["nr_of_lines"]):
        print("second checked")
        print(e)


def check_line_number(info):
    files = list_all_files_with_extension("selection/data/1. eerste ronde", ".xml")
    for file in files:
        name, number = file_to_name_and_number(file)
        for e in info:
            if e['name'] == name:
                if e["nr_of_lines"] < number:
                    print("Correction number to high: ")
                    print(e)



def check_info(info):
    for e in info:
        first_check_test(e)
        second_check_test(e)
        first_second_test(e)


    print("Totally checked")
    for e in info:
        totally_checked(e)

    check_line_number(info)


def find_duplicates(path):
    files = list_all_files_with_extension(path, ".xml")
    result = set()
    duplicates = set()
    for file in files:
        if file in result:
            print("duplicate")
            print(file)
            duplicates.add(file)
        else:
            result.add(file)
    return duplicates
