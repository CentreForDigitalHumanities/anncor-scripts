import sys, resource
from parse_check.compare_dirs import *

dir_1 = sys.argv[1]
dir_2 = sys.argv[2]
results_file = sys.argv[3]

tags = [
    "sentence",
]

selection = lambda x: "VanKampen" in x and ".xml" in x

ignore_characters = [
    ".",
    ",",
    "/",
    "?",
    "|",
    "xxx",
    " ",
    "'",
    '"',
    "\\",

]

#Python does not like recursion, this increases the max recursion limit
resource.setrlimit(resource.RLIMIT_STACK, (2**29,-1))
sys.setrecursionlimit(10**6)


result = compare_dirs(dir_1, dir_2, selection, tags, ignore_characters)

print_list_to_file(results_file, result)

