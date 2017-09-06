import math


def get_selection(scores, fraction):
    """
    Return the windowed selection with the highest score.

    Arguments:
    scores -- a list of scores and their index number (number,score)[]
    fraction -- the fraction size to select
    """
    subset_length = math.ceil(fraction * len(scores))
    return [] # TODO

def get_file_selection(files, fraction):
    """
    Return the files with the window selections having the highest score.

    Arguments:
    scores -- a list of filenames, scores and their index number (filename, (number,score)[])[]
    fraction -- the fraction size to select
    """
    return [] # TODO
