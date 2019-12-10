from cpu import CPU
from input_output import IO


class Data():
    def __init__(self):
        self.ready_queue = []
        self.cpu = CPU()
        self.io = IO()
        self.completed = []
        self.total_time = 0
        self.cpu_time = 0
        self.wait = dict()
        self.turn_around = dict()
        self.response = dict()
        self.mlfq = [[], [], []]
        self.qcounter = [0, 0]
        self.gantt = []