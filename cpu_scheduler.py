from data import Data
from output import print_finished, print_gantt_chart 
from fcfs import fcfs
from sjf import sjf
from mlfq import mlfq


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
