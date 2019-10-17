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


class IO():
    def __init__(self):
        self.io_list = []

    def add(self, process):
        self.io_list.append(process)

    def execute(self):
        for p in self.io_list:
            p[1][0] -= 1


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


# Information printed at each context switch for FCFS and SJF
def print_context_switch(data):
    print(f"""

Current Time: {data.total_time}
Next process on the CPU: {data.cpu.process[0] + ", Burst: " + str(data.cpu.process[1][0]) if data.cpu.process else "[idle]"}
..................................................................
List of processes in the ready queue:
\tProcess\t\tBurst""")
    for p in data.ready_queue:
        print(f"\t{p[0]}\t\t{p[1][0]}")
    if not data.ready_queue:
        print("\t[empty]")
    print(f"""
List of processes in I/O:
\tProcess\t\tRemaining I/O Time""")
    for p in data.io.io_list:
        print(f"\t{p[0]}\t\t{p[1][0]}")
    if not data.io.io_list:
        print("\t[empty]")
    print("..................................................................")
    print("Completed: ", end='')
    if data.completed:
        for c in sorted(data.completed):
            print(c, end=', ')
        print('\n')
    else:
        print("[empty]")
    print("::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")


# Printing the details of the final results
def print_detail(data_dict, title):
    print(f"{title} times:", end='\t\t')
    for k in sorted(data_dict.keys()):
        print(f"{k}", end='\t')
    print("\n\t\t\t", end='')
    for k in sorted(data_dict.keys()):
        print(f"{data_dict[k]}", end='\t')
    print(f"\nAve {title}:\t\t{sum(list(data_dict.values())) / len(data_dict)}\n")


# Information printed at the end of simulation
def print_finished(data):
    print("Finished\n")
    print(f"total_time:\t\t{data.total_time}")
    print(f"CPU utilization:\t{data.cpu.cpu_time / data.total_time * 100}%\n")

    print_detail(data.wait, "Wait")
    print_detail(data.turn_around, "T-around")
    print_detail(data.response, "Response")


# Print out raw gantt chart
def print_gantt_chart(data):
    for p in data.gantt:
        if p[0] == 'idle':
            print('|' + p[0], end='\t')
        else:
            print('|' + p[0], end='\t\t' )
    print('|idle')
    for t in data.gantt:
        print(t[1], end='\t\t')
    print(data.total_time)

# FCFS scheduling algorithm
def fcfs(data):
    context_switch = True
    idle = False
    while data.ready_queue or data.cpu.process or data.io.io_list:
        # check CPU first
        if not data.cpu.occupied and data.ready_queue:
            data.cpu.add(data.ready_queue.pop(0))
            if data.response[data.cpu.process[0]] < 0:  # record response time
                data.response[data.cpu.process[0]] = data.total_time
            context_switch = True
            idle = False
        else:
            context_switch = False

        if context_switch:
            print_context_switch(data)
            data.gantt.append((data.cpu.process[0], data.total_time))
        if not data.cpu.occupied and not data.ready_queue and not idle:
            data.gantt.append(('idle', data.total_time))
            idle = True

        data.total_time += 1  # time tick
        # execute current process on CPU
        if data.cpu.occupied:
            data.cpu.execute()
        # execute process on IO
        data.io.execute()

        # everyone else on ready_queue waits
        for p in list(data.ready_queue):
            data.wait[p[0]] += 1

        if not data.cpu.occupied and data.cpu.process:  # move process to IO, trigger context switch
            if data.cpu.process[1]:  # there are still CPU or IO left
                data.io.add(data.cpu.process)
            else:
                data.completed.append(data.cpu.process[0])
                data.turn_around[data.cpu.process[0]] = data.total_time  # record turn around time
            data.cpu.process = []

        # check IO, push completed process to ready_queue
        temp = data.io.io_list[:]
        data.io.io_list = []
        for p in temp:
            if p[1][0] == 0:  # completed IO process
                del p[1][0]
                data.ready_queue.append(p)
            else:
                data.io.io_list.append(p)

    print_context_switch(data)


# SJF scheduling algorithm
def sjf(data):
    context_switch = True
    idle = False
    while data.ready_queue or data.cpu.process or data.io.io_list:
        data.ready_queue.sort(key=lambda x: x[1][0])  # put shortest job at front
        # check CPU first
        if not data.cpu.occupied and data.ready_queue:
            data.cpu.add(data.ready_queue.pop(0))
            if data.response[data.cpu.process[0]] < 0:  # record response time
                data.response[data.cpu.process[0]] = data.total_time
            context_switch = True
            idle = False
        else:
            context_switch = False

        if context_switch:
            print_context_switch(data)
            data.gantt.append((data.cpu.process[0], data.total_time))
        if not data.cpu.occupied and not data.ready_queue and not idle:
            data.gantt.append(('idle', data.total_time))
            idle = True

        data.total_time += 1  # time tick
        # execute current process on CPU
        if data.cpu.occupied:
            data.cpu.execute()
        # execute process on IO
        data.io.execute()

        # everyone else on ready_queue waits
        for p in list(data.ready_queue):
            data.wait[p[0]] += 1

        if not data.cpu.occupied and data.cpu.process:  # move process to IO, trigger context switch
            if data.cpu.process[1]:  # there are still CPU or IO left
                data.io.add(data.cpu.process)
            else:
                data.completed.append(data.cpu.process[0])
                data.turn_around[data.cpu.process[0]] = data.total_time  # record turn around time
            data.cpu.process = []

        # check IO, push completed process to ready_queue
        temp = data.io.io_list[:]
        data.io.io_list = []
        for p in temp:
            if p[1][0] == 0:  # completed IO process
                del p[1][0]
                data.ready_queue.append(p)
            else:
                data.io.io_list.append(p)

    print_context_switch(data)


# Information printed at each context switch for MLFQ
def print_context_switch_mlfq(data):
    mlfq_names = ['Q1', 'Q2', 'Q3']
    print(f"""

Current Time: {data.total_time}
Next process on the CPU: {data.cpu.process[0] + ", Burst: " + str(data.cpu.process[1][0]) if data.cpu.process else "[idle]"}
..................................................................
List of processes in the ready queue:
\tProcess\t\tBurst\t\tQueue""")
    for q in data.mlfq:
        for p in q:
            print(f"\t{p[0]}\t\t{p[1][0]}\t\t{mlfq_names[p[2]]}")
    if not any(data.mlfq):
        print("\t[empty]")
    print(f"""
List of processes in I/O:
\tProcess\t\tRemaining I/O Time""")
    for p in data.io.io_list:
        print(f"\t{p[0]}\t\t{p[1][0]}")
    if not data.io.io_list:
        print("\t[empty]")
    print("..................................................................")
    print("Completed: ", end='')
    if data.completed:
        for c in sorted(data.completed):
            print(c, end=', ')
        print('\n')
    else:
        print("[empty]")
    print("::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::")


# MLFQ scheduling algorithm
def mlfq(data):
    context_switch = True
    idle = False
    while any(data.mlfq) or data.io.io_list or data.cpu.process:
        # check CPU first
        if not data.cpu.occupied or not data.cpu.process:
            for i, q in enumerate(data.mlfq):
                if q:
                    data.cpu.add(q.pop(0))
                    if i < 2:
                        data.qcounter[i] = 0
                    if data.response[data.cpu.process[0]] < 0:  # record response time
                        data.response[data.cpu.process[0]] = data.total_time
                    context_switch = True
                    idle = False
                    break
                else:
                    context_switch = False
        else:
            curr_process_priority = data.cpu.process[2]
            for i, q in enumerate(data.mlfq):
                if i < curr_process_priority and q:
                    # preemption
                    data.mlfq[curr_process_priority].append(data.cpu.process)
                    if curr_process_priority < 2:
                        data.qcounter[curr_process_priority] = 0
                    data.cpu.add(q.pop(0))
                    data.qcounter[i] = 0
                    if data.response[data.cpu.process[0]] < 0:  # record response time
                        data.response[data.cpu.process[0]] = data.total_time
                    context_switch = True
                    idle = False
                    break
            else:
                context_switch = False

        if context_switch:
            print_context_switch_mlfq(data)
            data.gantt.append((data.cpu.process[0], data.total_time))
        if not data.cpu.occupied and not any(data.mlfq) and not idle:
            data.gantt.append(('idle', data.total_time))
            idle = True


        data.total_time += 1  # time tick
        # execute current process on CPU
        if data.cpu.occupied:
            data.cpu.execute()
            if data.cpu.process[2] < 2:
                data.qcounter[data.cpu.process[2]] += 1
        # execute process on IO
        data.io.execute()

        # everyone else on ready_queue waits
        for q in data.mlfq:
            for p in q:
                data.wait[p[0]] += 1

        if not data.cpu.occupied and data.cpu.process:  # move process to other queue or io, trigger context switch
            if data.cpu.process[1]:  # there are still CPU or IO left
                data.io.add(data.cpu.process)
            else:
                data.completed.append(data.cpu.process[0])
                data.turn_around[data.cpu.process[0]] = data.total_time  # record turn around time
            if data.cpu.process[2] < 2:
                data.qcounter[data.cpu.process[2]] = 0
            data.cpu.process = []

        if data.qcounter[0] == 5 and data.cpu.occupied and data.cpu.process[2] == 0:
            # time quantum used up, downgrade
            data.cpu.process[2] = 1
            data.mlfq[1].append(data.cpu.process)
            data.cpu.process = []
            data.qcounter[0] = 0

        if data.qcounter[1] == 10 and data.cpu.occupied and data.cpu.process[2] == 1:
            # time quantum used up, downgrade
            data.cpu.process[2] = 2
            data.mlfq[2].append(data.cpu.process)
            data.cpu.process = []
            data.qcounter[1] = 0


        # check IO, push completed process to ready_queue
        temp = data.io.io_list[:]
        data.io.io_list = []
        for p in temp:
            if p[1][0] == 0:  # completed IO process
                del p[1][0]
                data.mlfq[p[2]].append(p)
            else:
                data.io.add(p)

    print_context_switch_mlfq(data)


# Main driver for program
def main():
    # Original
    bursts = [
        ['P1', [5, 27, 3, 31, 5, 43, 4, 18, 6, 22, 4, 26, 3, 24, 4]],
        ['P2', [4, 48, 5, 44, 7, 42, 12, 37, 9, 76, 4, 41, 9, 31, 7, 43, 8]],
        ['P3', [8, 33, 12, 41, 18, 65, 14, 21, 4, 61, 15, 18, 14, 26, 5, 31, 6]],
        ['P4', [3, 35, 4, 41, 5, 45, 3, 51, 4, 61, 5, 54, 6, 82, 5, 77, 3]],
        ['P5', [16, 24, 17, 21, 5, 36, 16, 26, 7, 31, 13, 28, 11, 21, 6, 13, 3, 11, 4]],
        ['P6', [11, 22, 4, 8, 5, 10, 6, 12, 7, 14, 9, 18, 12, 24, 15, 30, 8]],
        ['P7', [14, 46, 17, 41, 11, 42, 15, 21, 4, 32, 7, 19, 16, 33, 10]],
        ['P8', [4, 14, 5, 33, 6, 51, 14, 73, 16, 87, 6]]]


    data = Data()

    # initialize ready_queue and wait
    for p in bursts:
        data.mlfq[0].append(p + [0])
        data.ready_queue.append(p)
        data.wait[p[0]] = 0
        data.turn_around[p[0]] = 0
        data.response[p[0]] = -1

    # Choose which algorithm to perform
    fcfs(data)
    # sjf(data)
    # mlfq(data)
    print_finished(data)
    print_gantt_chart(data)



if __name__ == "__main__":
    main()
