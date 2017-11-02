import unittest
from utils.filesystem import *
import shutil


class TestFileSystem(unittest.TestCase):

    def setUp(self):
        self.dir_ref = "./utils/tests/test_files_filesystem/list_splited_paths_test"
        self.filelist_location = "./utils/tests/test_files_filesystem/file_lists"
    def test_sort_splited_paths(self):
        splited_paths = [
            ("/c", "b.xml"),
            ("/g", "d.xml"),
            ("/d", "a.xml"),
            ("/b", "c.xml"),

        ]

        result = sort_splited_paths_on_filename(splited_paths)
        self.assertEqual(
            result, [("/d", "a.xml"),
                     ("/c", "b.xml"),
                     ("/b", "c.xml"),
                     ("/g", "d.xml"), ]
        )

    def test_list_files_no_criteria(self):
        dir_ref = self.dir_ref
        files_rel_ref = [
            "1.xml",
            "2.xml",
            "3.xml",
            "4.xml",
            "1/11.xml",
            "1/12.xml",
            "2/21.xml",
            "2/22.xml",
            "2/text.txt",
        ]
        expected_refs = sorted([
            "{}/{}".format(dir_ref, ref) for ref in files_rel_ref
        ])
        result = sorted(list_files(dir_ref))
        self.assertEqual(expected_refs, result)

    def test_list_file_with_criteria(self):
        expected_refs = [
            "{}/2/text.txt".format(self.dir_ref)
        ]
        result = list_files(self.dir_ref, lambda x: x[len(x)-3:]=="txt")
        self.assertEqual(expected_refs, result)


    def test_create_filelists(self):
        files = sorted(list_files(self.dir_ref, lambda x: x[len(x)-3:]=="xml"))

        create_filelists(files, self.filelist_location, 4)
        dirs = [name for name in os.listdir(self.filelist_location)]
        self.assertEqual(len(dirs), 2)


    def tearDown(self):
        if os.path.isdir(self.filelist_location):
          shutil.rmtree(self.filelist_location)






