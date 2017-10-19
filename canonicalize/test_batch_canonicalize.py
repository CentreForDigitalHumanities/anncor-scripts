import unittest
from canonicalize.batch_canonicalize_functions import *


class TestBatchFunctions(unittest.TestCase):
    def setUp(self):
        self.dir_ref = "./canonicalize/files_with_errors/"

    def test_find_errors(self):
        results = find_errors(self.dir_ref, remove=False)
        self.assertEqual(len(results["no source node for index"]), 2)
        self.assertEqual(len(results["leaf node without @begin"]), 3)
        self.assertEqual(len(results["is used more than once"]), 0)

    def test_canonicalize_one_file(self):
        found_errors = {"sorting": []}
        canonicalize_one_file("./canonicalize/files_with_errors/VanKampen_laura44_u00000000130.xml", found_errors)
        print(found_errors)
        self.assertEqual(found_errors,
                         {"sorting": [('./canonicalize/files_with_errors/VanKampen_laura44_u00000000130.xml',
                                       'Exception: sorting conflict while sorting "./canonicalize/files_with_errors/VanKampen_laura44_u00000000130.xml"!\n')]})
