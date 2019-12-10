class IO():
    def __init__(self):
        self.io_list = []

    def add(self, process):
        self.io_list.append(process)

    def execute(self):
        for p in self.io_list:
            p[1][0] -= 1