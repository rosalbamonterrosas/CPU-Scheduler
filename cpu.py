class CPU():
    def __init__(self):
        self.process = []
        self.occupied = False
        self.cpu_time = 0

    def add(self, process):
        self.process = process
        self.occupied = True

    def execute(self):
        self.process[1][0] -= 1
        if self.process[1][0] == 0:
            del self.process[1][0]
            self.occupied = False
        self.cpu_time += 1