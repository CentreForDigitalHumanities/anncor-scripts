import os
import zipfile
import codecs
import time
from datetime import datetime, date

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


def list_all_files(path, extension):
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
   return list_all_files(path, ".cha")

def clean_file_name(file_name):
    file_name  = file_name.replace("VanKampen_", "")
    file_name = file_name.replace("uttfiles2_", "")
    i = file_name.find("_")
    return file_name[0:i]

def count_expressions(path):
    files = list_all_files(path, ".xml")
    result = {}
    #to make sure there are no duplicates
    found = set()
    for file in files:
        if file in found:
            pass
        else:
            found.add(file)
            file = clean_file_name(file)
            if file in result.keys():
                result[file] += 1
            else:
                result[file] = 1
    return result

def normalize_xml_files(path):
    files = list_all_files(path, ".xml")
    result = set([])
    for file in files:
        file = clean_file_name(file)
        result.add(file)
    return result


def unzip(path):
    zip_ref = zipfile.ZipFile(path, 'r')
    new_path = path[:-3]
    zip_ref.extractall(new_path)
    zip_ref.close()
    return new_path

def get_date(string):
    return string[7:-1]

def date_to_timestamp(date_string):
    ar = date_string.split("-")
    d = date(int(ar[2]), dates[ar[1]], int(ar[0]))
    return time.mktime(d.timetuple())

def create_info():
    path = "selection/data/cha-files"
    first_round = count_expressions("selection/data/1. eerste ronde")
    second_round = count_expressions("selection/data/2. afgerond")
    results = []
    for file in os.listdir(path):
        date = ""
        with codecs.open(os.path.join(path, file), "r", "utf-8") as f:
            count = 0
            for line in f.readlines():
                if("*" == line[0]):
                    count += 1
                if("@Date" in line):
                    date = date_to_timestamp(get_date(line))

        file = file[:-4]
        info = {
            "name": file,
            "time_stamp": date,
            "nr_of_lines": count,
            "first_check": first_round[file] if file in first_round else 0 ,
            "second_check": second_round[file] if file in second_round else 0
        }
        results.append(info)
    return results

def store_info(info, location):
    with open(location, "w") as f:
        for entry in info:
            json.dump(entry, f)
            f.write("\n")

def load_info(location):
    info = []
    with open(location, "r") as f:
        for line in f.readlines():
            info.append(json.loads(line))
    return info



