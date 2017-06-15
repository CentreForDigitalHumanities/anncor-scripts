#!/usr/bin/env python3
"""
Classes for modifying a file by line.
"""
class InjectableFile:
    """
    Open a file and allow new lines to be inserted into a copy of the file.
    Use write() to write the modified file with the inserted lines.
    Note: this assumes the read file did not change during operation.

    Attributes:
        line_modifications  A dictionary containing the modifications (if any) to be done for each
            line number.
    """
    def __init__(self, filename):
        self.file = open(filename, 'r')
        self.filename = filename
        self.line_modifications = {}

    def __del__(self):
        self.close()

    def close(self):
        """
        Close the file reader.
        """
        if self.file is not None:
            self.file.close()

    def read_lines(self, include_modifications=False):
        """
        Read the lines of a file.

        Args:
            include_modifications (bool): Whether the modification should be included or the file
                will be returned as is.

        Returns:
            A generator to iterate over all the lines of the file.
        """

        self.file.seek(0)
        line_number = 0
        for line in self.file:
            yield line.rstrip('\n')

            if include_modifications:
                modifications = self.line_modifications.get(line_number)
                if modifications:
                    for appended_line in modifications.after:
                        yield appended_line

                # only modified here, because it isn't used when just reading the file
                line_number += 1

    def append_at(self, line_number, *lines):
        """
        Append a line after a given line_number.

        Args:
            line_number: The zero-based line number after which the line(s) will be appended.
        """
        existing_modification = self.line_modifications.get(line_number)

        if not existing_modification:
            existing_modification = LineModifications()
            self.line_modifications[line_number] = existing_modification

        for line in lines:
            existing_modification.after.append(line)

class LineModifications:
    """
    Represent the modifications to be performed to a file line.

    Attributes:
        after   The lines to be placed after the original line.
    """
    def __init__(self):
        self.after = []
