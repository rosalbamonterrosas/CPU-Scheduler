# CPU Scheduler
Simulation of FCFS, SJF, and MLFQ CPU scheduling algorithms. 

## Information displayed for each context switch
* Current Execution time  
* Running process  
* The Ready queue, with the CPU burst time for each process   
* The Processes in I/O with the remaining time for every process for its I/O burst completion  
* Indication when a process has completed its total execution    

## Results printed at the end of simulation
* Total time needed to complete all 8 processes  
* CPU utilization  
* Waiting times for each process and the average waiting time for all processes (Tw)  
* Turnaround time for each process and the average turnaround time (Ttr)  
* Response time for each process and the average response time (Tr)  

## To run the CPU Scheduler, follow the steps below:
* Clone the repo: `https://github.com/rosalbamonterrosas/CPU-Scheduler.git`
* `cd CPU-Scheduler`
* Run the CPU Scheduler: `python3 cpu_scheduler.py`
