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