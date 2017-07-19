from selection.evo_alg import *
import numpy as np
from selection.file_parser import *

class SelectionProblem(Problem):
    def __init__(self, data_path, weights=[1,1,1,1,1,], min_percentage_files=10, max_percentage_files=20, max_lines_to_check=np.inf):
        self.selection_data = load_info(data_path)
        self.total_lines = self.get_total_lines(self.selection_data)
        self.total_files = len(self.selection_data)
        self.proportion = 74/50
        self.weights = weights
        self.min_percentage_files = min_percentage_files
        self.max_percentage_files = max_percentage_files
        self.max_lines_to_check=max_lines_to_check

    def setWeights(self, weights):
        self.weights = weights

    def get_random_solution(self):
        nr_of_files = round(((self.max_percentage_files - self.min_percentage_files) * np.random.rand()) + self.min_percentage_files) * self.total_files / 100
        solution = np.random.choice(self.selection_data, int(nr_of_files), replace=False)
        return solution

    def mate(self, sol1, sol2):
        sol1s = set([s["name"] for s in sol1])
        sol2s = set([s["name"] for s in sol2])
        sol3s = list(sol1s.union(sol2s))
        sol3 = np.concatenate([sol1, sol2])

        solution = np.random.choice(sol3s, max([len(sol1), len(sol2)]), replace=False)
        result = []
        for s in solution:
            for i in range(0, len(sol3)):
                if sol3[i]["name"] == s:
                    result.append(sol3[i])
                    break
        return result

    def fitness_function(self, solution):
        if(self.violates_hard_constraints(solution)):
            return -np.inf
        score = self.get_score(solution)

        return np.dot(self.weights, score)

    def violates_hard_constraints(self, solution):
        return self.check_line_constraints(solution)

    def check_line_constraints(self, solution):
        return self.get_total_lines_to_check(solution) > self.max_lines_to_check

    def get_score(self, solution):
        return  [
            self.get_percentage_score(solution),
            self.get_proportion_score(solution),
            self.get_uniformity_score(solution),
            self.get_first_check_score(solution),
            self.get_second_check_score(solution)
        ]
    def get_percentage_score(self, solution):
        return self.get_line_percentage(solution)

    #Proportion between laura and sarah files
    def get_proportion_score(self, solution):
        return 1/(1 + self.proportion_error(solution))

    #Score of how uniform the solution is over time
    def get_uniformity_score(self, solution):
        sorted_solution = solution
        n = len(sorted_solution)
        ideal = SelectionProblem.get_ideal_uniformity(sorted_solution[0]["time_stamp"], sorted_solution[n-1]["time_stamp"], n)
        timestamps = [e["time_stamp"] for e in solution]
        return -(SelectionProblem.sum_difference_ideal_actual_dates(ideal, timestamps) / (30**8))

    #Percentage of firsted checked
    def get_first_check_score(self, solution):
        return self.get_total_first_checked(solution)/self.get_total_lines(solution)

    #Percentage of second checked
    def get_second_check_score(self, solution):
        return self.get_total_second_checked(solution)/self.get_total_lines(solution)


    #How many lines are covered in total
    def get_line_percentage(self, solution):
        nr_lines = self.get_total_lines(solution)
        return nr_lines/self.total_lines


    def proportion_error(self, solution):
        proportion = self.get_proportion(solution)
        if proportion == -1:
            return np.inf
        return (self.proportion - proportion)**2


    def get_mean_differences(self, solution):
        sarah_solution = [e for e in solution if "sarah" in e["name"]]
        laura_solution = [e for e in solution if "laura" in e["name"] ]
        if len(sarah_solution) != 0:
            sarah_mse = self.get_mean_square_error_date_difs(sarah_solution)
        else:
            sarah_mse = -np.inf
        if len(laura_solution) != 0:
            laura_mse = self.get_mean_square_error_date_difs(laura_solution)
        else:
            laura_mse = -np.inf
        return 1 / (1+ laura_mse + sarah_mse)

    def get_date_differences(self, solution):
        difs = []
        for i in range(0, len(solution) - 1):
            difs.append(solution[i + 1]["time_stamp"] - solution[i]["time_stamp"])
        return difs

    def get_mean_square_error_date_difs(self, solution):
        s = sorted(solution , key = lambda e: e["time_stamp"] )
        difs = self.get_date_differences(s)
        if(len(difs) == 0):
            return -np.inf
        mean = sum(difs)/len(difs)
        error = [(d - mean)**2 for d in difs]
        mse = sum(error)
        return mse

    def get_proportion(self, solution):
        laura = sum("laura" in e["name"] for e in solution)
        sarah = sum("sarah" in e["name"] for e in solution)
        if sarah == 0:
            return -1
        else:
            return laura/sarah

    def get_total_lines(self,data):
        total_lines = 0
        for entry in data:
            total_lines += entry["nr_of_lines"]
        return total_lines

    def get_total_first_checked(self,data):
        return self.count_attr(data, "first_check")

    def get_total_second_checked(self,data):
        return self.count_attr(data, "second_check")

    def count_attr(self,data, attr):
        count = 0
        for entry in data:
            count += entry[attr]
        return count

    def check_double(self,solution):
        names = set([])
        for entry in solution:
            if entry["name"] in names:
                return True
            names.add(entry["name"])
        return False

    def get_lines_to_check_second(self,solution):
        return self.count_attr(solution, "nr_of_lines") - self.count_attr(solution, "second_check")

    def get_lines_to_check_first(self,solution):
        return self.count_attr(solution, "nr_of_lines") - self.count_attr(solution, "first_check")

    def get_total_lines_to_check(self, solution):
        return self.get_lines_to_check_second(solution) + 2 * self.get_lines_to_check_first(solution)

    def get_lines_checked_first(self, solution):
        return  self.count_attr(solution, "first_check")

    def get_lines_checked_second(self, solution):
        return  self.count_attr(solution, "second_check")


    def get_summary_of_name(self,solution, name):
        name_solution = [e for e in solution if name in e["name"]]
        dates = [datetime.fromtimestamp(int(e["time_stamp"])).strftime('%Y-%m-%d') for e in name_solution]

        return {"nr_of_files": len(name_solution), "nr_of_lines": self.count_attr(name_solution, "nr_of_lines"), "dates": dates}


    @staticmethod
    def sort_solution_date(solution):
        return sorted(solution, key = lambda e: e["time_stamp"], reverse=True)

    @staticmethod
    def sort_solution_name(solution):
        return sorted(solution, key = lambda e: e["name"])

    def get_summary(self, solution):
        laura_summary = self.get_summary_of_name_str(solution, "laura")
        sarah_summary = self.get_summary_of_name_str(solution, "sarah")
        to_check_first = self.get_lines_to_check_first(solution)
        to_check_second = self.get_lines_to_check_second(solution)
        checked_first = self.get_lines_checked_first(solution)
        checked_second = self.get_lines_checked_second(solution)
        return '''
    Summary:
        Violates Constraints:
            {}
        percentage lines checked: 
            {}
        number of lines to check: 
            {}
            first (and second):
                {}
            second:
                {}
        number of lines checked:
            {}
            first time:
                {}
            first and second time:
                {}
        '''.format(self.violates_hard_constraints(solution), self.get_percentage_score(solution), 2 * to_check_first+to_check_second, to_check_first, to_check_second,
                   checked_first + checked_second, checked_first, checked_second) + laura_summary + sarah_summary

    def get_summary_of_name_str(self, solution, name):
        summary = self.get_summary_of_name(solution, name)
        return '''
            {}:
                files:
                    {}
        '''.format(name, summary["nr_of_files"])


    def print_summary(self, solution):
        laura_summary = self.get_summary_of_name(solution, "laura")
        sarah_summary = self.get_summary_of_name(solution, "sarah")
        print("Laura: ")
        self.print_summary_name(laura_summary)
        print("Sarah: ")
        self.print_summary_name(sarah_summary)
        print("percentage lines checked: ")
        print("\t" + str(self.get_percentage_score(solution)))
        print(" Lines to check: ")
        print("\t First:")
        print("\t\t" + str(self.get_lines_to_check_first(solution)))
        print("\tSecond:")
        print("\t\t" + str(self.get_lines_to_check_second(solution)))
        print(" lines checked:")
        print("\t  First:")
        print("\t \t " + str(self.count_attr(solution, "first_check")))
        print("\t  Second:")
        print("\t \t" + str(self.count_attr(solution, "second_check")))

    def print_summary_name(self, summary):
        print("\tfiles: ")
        print("\t \t" + str(summary["nr_of_files"]))
        print("\tlines: ")
        print("\t \t" + str(summary["nr_of_lines"]))
        print("\tdates: ")
        print("\t \t" + str(sorted(summary["dates"])))

    def print_file_names(self, solution):
        names = [e["name"] for e in solution]
        print(names)

    @staticmethod
    def get_ideal_uniformity(start_date, end_date, number_of_samples):

        # Make sure we get something that could contain uniformity
        if (number_of_samples < 2 or end_date == start_date):
            return [np.inf for e in range(0, number_of_samples)]

        time_between_samples = (end_date - start_date) / (number_of_samples - 1)

        return [d for d in np.arange(start_date, end_date + 1, time_between_samples)]

    @staticmethod
    def sum_difference_ideal_actual_dates(ideal_timestamps, actual_timestamps):
        """"Compares the ideal distribution with the actual distribution of dates
            both ideal and actual should be timestamps
            ideal and actual should be same size
            returns the mean square error of the ideal dates compared to the actual dates
        """
        ideal_sorted = sorted(ideal_timestamps)
        actual_sorted = sorted(actual_timestamps)
        sum_difference = 0
        for i in range(len(ideal_sorted)):
            sum_difference += abs(ideal_sorted[i] - actual_sorted[i])
        return sum_difference

    def to_string(self):
        return '''  "percentage_weight": "{}", "proportion_weight": "{}", "uniformity_weight": "{}", "first_check_weight": "{}", "second_check_weight": "{}
    "max_lines_to_check": "{}", "min_percentage_files": "{}", "max_percentage_files": "{}"'''.format(self.weights[0], self.weights[1], self.weights[2], self.weights[3], self.weights[4], self.max_lines_to_check, self.min_percentage_files, self.max_percentage_files)

            #'{"percentage_weight": "{}",  "proportion_weight": "{}", "uniformity_weight": "{}", first_check_weight: "{}", "second_check_weight": "{}"}'.format(self.weights[0],self.weights[1],self.weights[2],self.weights[3],self.weights[4])

