
import unittest
from ..window import get_file_selection, get_selection


class TestWindow(unittest.TestCase):
    def generate_files(self, scores):
        return [self.generate_file('file{0}'.format(i), file_scores) for i, file_scores in enumerate(scores)]

    def generate_file(self, name, scores):
        return (name, [(i, score) for i, score in enumerate(scores)])

    def test_window(self):
        result = get_selection([
            (1, 0),
            (2, 0),
            (3, 2),
            (4, 0),
            (5, 1),
            (6, 2),
            (7, 1),
            (8, 2),
            (9, 1),
            (10, 0),
            (11, 0),
            (12, 1)],
            0.3)
        self.assertEqual(result, [range(5, 9)])

    def test_files_window(self):
        data = self.generate_files(
            [
                # begin
                [2, 2, 2, 2, 0, 0, 0, 1, 0, 0, 1, 2],
                # middle
                [0, 0, 2, 0, 1, 2, 1, 2, 1, 0, 0, 1],
                # end
                [0, 1, 0, 2, 0, 1, 0, 2, 2, 1, 2, 1]
            ]
        )

        results = get_file_selection(data, 0.3)
        self.assertEqual(len(results), 1)
        self.assert_file(results[0], "file0", 0, 4)
        self.assert_file(results[0], "file1", 4, 8)
        self.assert_file(results[0], "file2", 8, 12)

    def assert_file(self, result, expected_filename, start, end):
        (actual_filename, utterances) = result
        self.assertEqual(actual_filename, expected_filename)
        self.assertEqual(utterances, [range(start, end)])
