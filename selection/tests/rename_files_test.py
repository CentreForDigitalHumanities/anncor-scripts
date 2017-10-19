import unittest
from ..scripts.rename_files import *


class TestRenameFiles(unittest.TestCase):
    def test_create_new_name(self):
        old_name = "VanKampen_laura01_u00000000001.xml"
        new_name = create_new_name(old_name)
        expected = "VanKampen_laura01_u00000000000.xml"
        self.assertEqual(new_name, expected)
