class Data:
    data = []

    def parse_input(self, input_data):
        for line in input_data.split("\n"):
            split_line = line.split(',')
            if len(split_line) == 1:
                continue
            self.data.append(line.split(','))
