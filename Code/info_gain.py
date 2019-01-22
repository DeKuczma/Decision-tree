import math
from collections import defaultdict


class InfoGain:

    def calculate_gain(self, attribute, data, valid_rows, prev_entropy):
        default_rows = defaultdict(list)
        for i in valid_rows:
            default_rows[data.data[i][attribute]].append(i)
        entropy = 0
        valid_len = len(valid_rows)
        for key in default_rows:
            temp_entropy = self.calculate_entropy(attribute, data, default_rows[key])
            entropy += (temp_entropy * len(default_rows[key]) / valid_len)
        new_entropy = prev_entropy - entropy
        return new_entropy

    @staticmethod
    def calculate_entropy(attribute, data, valid_rows):
        final_values = dict()
        data_len = len(valid_rows)
        for i in valid_rows:
            value = data.data[i][len(data.data[0]) - 1]
            final_values[value] = final_values.get(value, 0) + 1.0
        entropy = 0
        for key in final_values:
            p = final_values[key] / data_len
            entropy -= (p * math.log(p, 2))
        return entropy


class GainRatio:

    def calculate_gain(self, attribute, data, valid_rows, prev_entropy):
        info_gain = InfoGain()
        gain = info_gain.calculate_gain(attribute, data, valid_rows, prev_entropy)
        split = self.calculate_split(attribute, data, valid_rows)
        return gain/split

    @staticmethod
    def calculate_split(attribute, data, valid_rows):
        final_values = dict()
        data_len = len(valid_rows)
        for i in valid_rows:
            value = data.data[i][attribute]
            final_values[value] = final_values.get(value, 0) + 1

        entropy = 0
        for key in final_values:
            p = final_values[key] / data_len
            entropy -= p * math.log(p, 2)
        return entropy
