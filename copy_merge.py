#!/usr/bin/env python3
"""
Copy files recursively from [source] to [target]. Replacing all files, matching by filename, from [replacements] (recursively).
"""

from shutil import copyfile
import glob
import os
import sys
source_directory = sys.argv[1]
target_directory = sys.argv[2]
replacements_directory = sys.argv[3]

# index all the replacement files
replacement_filepaths = {}
for filepath in glob.glob(os.path.join(replacements_directory, '**', '*.*'), recursive=True):
    replacement_filepaths[os.path.split(filepath)[1]] = filepath

# loop through the source structure directories
for filepath in glob.glob(os.path.join(source_directory, '**', '*.*'), recursive=True):
    filename = os.path.split(filepath)[1]
    if filename in replacement_filepaths:
        source = replacement_filepaths[filename]
    else:
        source = filepath
    target = os.path.join(target_directory, os.path.relpath(filepath, source_directory))
    os.makedirs(os.path.dirname(target), exist_ok=True)
    copyfile(source, target)
