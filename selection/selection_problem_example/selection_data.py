import numpy as np

class SelectionData:
    def __init__(self, data):
        self.data = data

    def get_random_from_year(self, year):
        month = np.random.choice([key for key in self.data[year]])
        return self.data[year][month]
