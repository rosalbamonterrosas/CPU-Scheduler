from output import print_context_switch_mlfq


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