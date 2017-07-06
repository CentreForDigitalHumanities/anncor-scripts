import unittest

from selection.selection_problem import SelectionProblem
from ..evo_alg import *
from ..file_parser import *


class testSelectionProblem(unittest.TestCase):

    def test_get_solution(self):
        p = SelectionProblem("selection/info.txt")
        solution = get_solution(p, 100, 100, 10)
        s= sorted(solution,  key = lambda e: e["time_stamp"])
        print([e["name"] for e in s])
        self.print_solution_statistics(p, solution)


    def print_solution_statistics(self, p, solution):
        print("lines to check second time: ")
        print(p.get_lines_to_check_second(solution))
        print("lines to check first time: ")
        print(p.get_lines_to_check_first(solution))
        laura_summary = p.get_summary_of_name(solution, "laura")
        sarah_summary = p.get_summary_of_name(solution, "sarah")
        print("Laura: ")
        self.print_summary(laura_summary)
        print("Sarah: ")
        self.print_summary(sarah_summary)


    def print_summary(self, summary):
        print("\tfiles: ")
        print("\t" + str(summary["nr_of_files"]))
        print("\tlines: ")
        print("\t" + str(summary["nr_of_lines"]))
        print("\tdates: ")
        print("\t" + str(sorted(summary["dates"])))

    def test_get_ideal_uniformity(self):
        start_date = self.date_to_timestamp("01/01/2000")
        end_date = self.date_to_timestamp("01/01/2004")
        nr_of_samples = 5

        expected = [
           "2000-01-01 00:00:00",
           "2000-12-31 06:00:00",
           "2001-12-31 12:00:00",
           "2002-12-31 18:00:00",
           "2004-01-01 00:00:00"
        ]

        result = SelectionProblem.get_ideal_uniformity(start_date, end_date, nr_of_samples)
        result = [self.timestamp_to_date(e) for e in result]
        self.assertEqual(expected, result)

    def test_sum_difference_ideal_actual_dates(self):
        ideal = [1,2,3]
        actual = [1,2,4]
        result = SelectionProblem.sum_difference_ideal_actual_dates(ideal, actual)
        self.assertEqual(result, 1)
        ideal = [1, 2, 3]
        actual = [2, 3, 4]
        result = SelectionProblem.sum_difference_ideal_actual_dates(ideal, actual)
        self.assertEqual(result, 3)

    def date_to_timestamp(self, date):
        return time.mktime(datetime.strptime(date, "%d/%m/%Y").timetuple())

    def timestamp_to_date(self, timestamp):
        return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')