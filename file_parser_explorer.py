from selection.file_parser import *


info = load_info("selection/info.txt")
info2 = load_info("selection/new_info.txt")

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


for e in info:
    first_check_test(e)
    second_check_test(e)
    first_second_test(e)


print("Totally checked")
for e in info:
    totally_checked(e)

def find_duplicates(path):
    files = list_all_files(path, ".xml")
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


path = "selection/data/1. eerste ronde"

#dups = find_duplicates(path)
#print(dups)


