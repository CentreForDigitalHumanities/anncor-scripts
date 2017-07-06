import os
import zipfile
import codecs
import time
from datetime import datetime, date
import re

import json

dates = {
    "JAN": 1,
    "FEB": 2,
    "MAR": 3,
    "APR": 4,
    "MAY": 5,
    "JUN": 6,
    "JUL": 7,
    "AUG": 8,
    "SEP": 9,
    "OCT": 10,
    "NOV": 11,
    "DEC": 12
}


def create_info():
    """"
        Creates the information foor each cha files. This information includes: "name, time_stamp, nr_of_lines. nr_of_first_checked, nr_of_second_checked"
    """
    path = "selection/data/cha-files"

    first_round = get_lines_checked("selection/data/1. eerste ronde")
    second_round = get_lines_checked("selection/data/2. afgerond")

    count = 0
    for k in second_round:
        for entry in second_round[k]:
            if( entry not in first_round[k] and entry[0] != "sarah46"):
                count +=1
                print(entry)
    print(count)
    results = []

    #Count the lines and get the dates out of the files
    for file in os.listdir(path):
        date = ""
        with codecs.open(os.path.join(path, file), "r", "utf-8") as f:
            count = 0
            for line in f.readlines():
                if("*" == line[0]):
                    count += 1
                if("@Date" in line):
                    date = date_to_timestamp(get_date(line))

        #Remove the .cha extension
        file = file[:-4]
        info = {
            "name": file,
            "time_stamp": date,
            "nr_of_lines": count,
            "first_check": len(first_round[file]) if file in first_round else 0 ,
            "second_check": len(second_round[file]) if file in second_round else 0
        }

        results.append(info)
    return results


def list_all_files(path, extension):
    """"
        Lists all the files in the path with the given extension, when there is a zip folder it unzips it and removes the zip folder
    """
    files = []
    for file in os.listdir(path):
        if file.endswith(extension):
            files.append(file)
        if file.endswith(".zip"):
            new_path = unzip(os.path.join(path, file))
            os.remove(os.path.join(path, file))
            files = files + list_all_files(new_path, extension)
        # Dive into subfolders.
        if os.path.isdir(os.path.join(path, file)):
            files = files + list_all_files(os.path.join(path, file), extension)
    return files

def list_cha_files(path):
   """"
        List all the cha files in a given path
   """
   return list_all_files(path, ".cha")

def clean_file_name(file_name):
    """"
        Cleanes a file such that it only contains the name of the session
    """
    file_name  = file_name.replace("VanKampen_", "")
    file_name = file_name.replace("uttfiles2_", "")
    i = file_name.find("_")
    return file_name[0:i]

def get_number_from_file(file):
    """"
        Get the line number that this file annotates
    """
    #First delete everything before the numbers
    occurences = [m.start() for m in re.finditer('_', file)]
    number = file[occurences[-1] + 1:]
    if("u" in file):
        number = number[1:]
    number = int(number)
    return number

def file_to_name_and_number(file):

    #Examplaar is a file that we do not need to concern ourselfs with.
    if("Exemplaar" in file):
        return ( "", -1)
    name = clean_file_name(file[:-4])
    number = get_number_from_file(file[:-4])
    return (name, number)


def get_lines_checked(path):
    files = list_all_files(path, ".xml")
    result = {}
    found = set()
    for file in files:
        name_number = file_to_name_and_number(file)
        if name_number in found:
            pass
        else:
            found.add(name_number)
        if (not "uttfiles2_" in file):
            file = clean_file_name(file)
            if file in result.keys():
                result[file].add(name_number)
            else:
                result[file] = set([name_number])
    return result


def count_expressions(path):
    files = list_all_files(path, ".xml")
    result = {}
    #to make sure there are no duplicates
    found = set()
    for file in files:
        name_number = file_to_name_and_number(file)
        if name_number in found:
            if(name_number[0] == "laura47"):
                print(file)
                print(name_number)
            pass
        else:
            found.add(name_number)
            if(not "uttfiles2_" in file):
                file = clean_file_name(file)
                if file in result.keys():
                    result[file] += 1
                else:
                    result[file] = 1
            else:
                print(file)
    return result

def normalize_xml_files(path):
    files = list_all_files(path, ".xml")
    result = set([])
    for file in files:
        file = clean_file_name(file)
        result.add(file)
    return result


#Unzips all the zips in the path
def unzip(path):
    zip_ref = zipfile.ZipFile(path, 'r')
    new_path = path[:-3]
    zip_ref.extractall(new_path)
    zip_ref.close()
    return new_path

#Get the date out of a date string from a cha file
def get_date(string):
    return string[7:-1]


def date_to_timestamp(date_string):
    ar = date_string.split("-")
    d = date(int(ar[2]), dates[ar[1]], int(ar[0]))
    return time.mktime(d.timetuple())



def store_info(info, location):
    """"
        Stores the given info in the given location
    """
    with open(location, "w") as f:
        for entry in info:
            json.dump(entry, f)
            f.write("\n")

def load_info(location):
    """"
        Loads the info from the given location
    """
    info = []
    with open(location, "r") as f:
        for line in f.readlines():
            info.append(json.loads(line))
    return info



