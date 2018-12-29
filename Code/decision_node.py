class DecisionNode:

    def __init__(self, value, number):
        self.attribute = None
        self.value = value
        self.next_node = dict()
        self.node_number = number

    def add_next_node(self, attribute, node):
        self.next_node[attribute] = node

    def set_final_value(self, final_value):
        self.value = final_value

    def set_attribute(self, attribute):
        self.attribute = attribute
