"""
Windowed file selection: select a range from a file with the highest associated total score.
Notes:
- Utterance scores are assumed to be integer, which can be safely added/subtracted indefinitely
- If multiple selections exist with the maximum score, the first will be returned
"""
import math


def get_selection(utterances, fraction):
    """
    Return the windowed selection with the highest score.

    Arguments:
    utterances -- a list of utterance numbers and their scores (number,score)[]
    fraction -- the fraction size to select
    """
    subset_length = math.ceil(fraction * len(utterances))

    window = utterances[:subset_length]
    # the initial window might be the highest scoring
    selection = list(window)
    window_score = sum(score for number, score in window)
    highest_score = window_score

    for (utterance_number, utterance_score) in utterances[subset_length:]:
        (_, first_score) = window.pop(0)
        window_score -= first_score - utterance_score
        window.append((utterance_number, utterance_score))
        if window_score > highest_score:
            selection = list(window)
            highest_score = window_score

    return list(number for number, score in selection)


def get_file_selection(files, fraction):
    """
    Return the files with the window selections having the highest score.

    Arguments:
    files -- a list of filenames, utterances number and their scores (filename, (number,score)[])[]
    fraction -- the fraction size to select
    """
    return [(filename, get_selection(utterances, fraction)) for filename, utterances in files]
