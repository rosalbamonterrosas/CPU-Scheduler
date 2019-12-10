from output import print_context_switch


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