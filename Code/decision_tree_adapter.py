import Code.info_gain as info
import Code.attribute as attribute
import math
from collections import defaultdict
from Code.decision_node import DecisionNode
from copy import copy


class DecisionTreeAdapter:
    used = []
    root = attribute.Data()
    input_len = 0
    node_created = 0

    def __init__(self, config):
        self.config = config
        self.input_data = attribute.Data()
        self.info_gain = self.get_info_gain_type()

    def run(self):
        self.parse_input(self.config["file"])
        self.input_len = len(self.input_data.data[0]) - 1
        for i in range(self.input_len):
            self.used.append(False)
        valid_rows = []
        for i in range(len(self.input_data.data)):
            valid_rows.append(i)
        self.root = self.create_node(valid_rows, self.get_most_common_value(valid_rows))

    def parse_input(self, file):
        with open(file, 'r') as my_file:
            data = my_file.read()
        self.input_data.parse_input(data)

    def get_info_gain_type(self):
        if self.config["infoGain"]:
            return info.InfoGain()
        return info.GainRatio()

    def create_node(self, valid_rows, most_common_value):
        prev_entropy = self.calculate_entropy(valid_rows)
        if self.different_values(valid_rows):
            new_node = None
            new_node = DecisionNode("0", self.node_created)
            self.node_created += 1
            new_node.set_final_value(self.get_most_common_value(valid_rows))
            return new_node

        chosen_att = None
        chosen_entropy = None
        for i in range(len(self.used)):
            if self.used[i] is False:
                if chosen_att is None:
                    chosen_att = i
                    chosen_entropy = self.info_gain.calculate_gain(chosen_att, self.input_data, valid_rows, prev_entropy)
                else:
                    temp_entropy = self.info_gain.calculate_gain(i, self.input_data, valid_rows, prev_entropy)
                    if temp_entropy > chosen_entropy:
                        chosen_att = i
                        chosen_entropy = temp_entropy

        if chosen_entropy < self.config["minInfoGain"]:
            new_node = DecisionNode("0", self.node_created)
            self.node_created += 1
            new_node.set_final_value(self.get_most_common_value(valid_rows))
            return new_node

        self.used[chosen_att] = True

        new_node = DecisionNode("0", self.node_created)
        self.node_created += 1
        new_node.set_attribute(chosen_att)
        diff_attributes = defaultdict(list)
        all_values = dict()
        for i in self.input_data.data:
            all_values[i[chosen_att]] = 0
        for i in valid_rows:
            diff_attributes[self.input_data.data[i][chosen_att]].append(i)
        for key in all_values:
            if key in diff_attributes.keys():
                new_node.add_next_node(key, self.create_node(diff_attributes[key], self.get_most_common_value(diff_attributes[key])))
            else:
                temp_node = DecisionNode(most_common_value, self.node_created)
                self.node_created += 1
                new_node.add_next_node(key, temp_node)

        self.used[chosen_att] = False
        return new_node

    def different_values(self, valid_rows):
        if len(valid_rows) == 0:
            return False
        index = len(self.input_data.data[0]) - 1
        value = self.input_data.data[valid_rows[0]][index]
        for i in valid_rows:
            if self.input_data.data[i][index] != value:
                return False
        return True

    def calculate_entropy(self, valid_rows):
        final_values = dict()
        data_len = len(valid_rows)
        for i in valid_rows:
            value = self.input_data.data[i][self.input_len]
            final_values[value] = final_values.get(value, 0) + 1

        entropy = 0
        for key in final_values:
            p = final_values[key] / data_len
            entropy -= p * math.log(p, 2)
        return entropy

    def get_most_common_value(self, valid_rows):
        final_values = dict()
        for i in valid_rows:
            value = self.input_data.data[i][self.input_len]
            final_values[value] = final_values.get(value, 0) + 1

        result = None
        value = None
        for key in final_values:
            if value is None or final_values[key] > value:
                result = key
                value = final_values[key]
        return result
