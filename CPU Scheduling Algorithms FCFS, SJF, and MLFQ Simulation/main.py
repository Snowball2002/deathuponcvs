
DATA = {
    'P1': [5, 27, 3, 31, 5, 43, 4, 18, 6, 22, 4, 26, 3, 24, 4],
    'P2': [4, 48, 5, 44, 7, 42, 12, 37, 9, 76, 4, 41, 9, 31, 7, 43, 8],
    'P3': [8, 33, 12, 41, 18, 65, 14, 21, 4, 61, 15, 18, 14, 26, 5, 31, 6],
    'P4': [3, 35, 4, 41, 5, 45, 3, 51, 4, 61, 5, 54, 6, 82, 5, 77, 3],
    'P5': [16, 24, 17, 21, 5, 36, 16, 26, 7, 31, 13, 28, 11, 21, 6, 13, 3, 11, 4],
    'P6': [11, 22, 4, 8, 5, 10, 6, 12, 7, 14, 9, 18, 12, 24, 15, 30, 8],
    'P7': [14, 46, 17, 41, 11, 42, 15, 21, 4, 32, 7, 19, 16, 33, 10],
    'P8': [4, 14, 5, 33, 6, 51, 14, 73, 16, 87, 6]
}


def show_results(algorithm, results):
    print(f"\n--- {algorithm} Summary ---")
    total_waiting_time = 0
    total_turnaround_time = 0
    total_response_time = 0
    num_processes = len(results)

    for pid, result in results.items():
        wait_time = result['completion'] - sum(DATA[pid])  # Calculate waiting time
        turnaround = result['completion']
        response = result['response']
        total_waiting_time += wait_time
        total_turnaround_time += turnaround
        total_response_time += response

        print(f"{pid} - Waiting: {wait_time} Turnaround: {turnaround} Response: {response}")

    print(f"\nAverage Waiting Time: {total_waiting_time / num_processes}")
    print(f"Average Turnaround Time: {total_turnaround_time / num_processes}")
    print(f"Average Response Time: {total_response_time / num_processes}")
    cpu_utilization = (total_turnaround_time / (total_turnaround_time + total_waiting_time)) * 100
    print(f"CPU Utilization: {cpu_utilization:.2f}%\n")


# FFFFFFFFFFCCCCCCCCCCCCFFFFFFFFFSSSSSSSSSSSSSSSS
def fcfs_scheduler(processes):
    print("\nRunning FCFS Scheduler")
    current_time = 0
    results = {pid: {'completion': 0, 'response': 0} for pid in processes}

    for pid, bursts in processes.items():
        if results[pid]['response'] == 0:
            results[pid]['response'] = current_time
        current_time += sum(bursts)
        results[pid]['completion'] = current_time

    show_results("FCFS", results)


# SSSSSSSSSSJJJJJJFFFFFFFFFFF
def sjf_scheduler(processes):
    print("\nRunning SJF Scheduler")
    current_time = 0
    ready_list = []
    results = {pid: {'wait_time': 0, 'turnaround': 0, 'response': 0, 'completion': 0} for pid in processes}

    process_copy = {pid: bursts[:] for pid, bursts in processes.items()}

    while process_copy:
        for pid, bursts in list(process_copy.items()):
            if bursts and bursts[0] <= current_time:
                ready_list.append((pid, bursts.pop(0)))
                if not bursts:
                    del process_copy[pid]

        if ready_list:
            ready_list.sort(key=lambda x: x[1])
            pid, cpu_burst = ready_list.pop(0)
            results[pid]['response'] = max(current_time - results[pid]['completion'], 0) if results[pid][
                                                                                                'response'] == 0 else \
            results[pid]['response']
            current_time += cpu_burst
            results[pid]['completion'] = current_time
            if pid in process_copy:
                if not process_copy[pid]:
                    results[pid]['turnaround'] = current_time
                    del process_copy[pid]
        else:
            current_time += 1
    show_results("SJF", results)


# MMMMMMMMMMMMMMLLLLLLLLFFFFFFFFFFFFQQQQQQQQQQ
def mlfq_scheduler(processes):
    print("\nRunning MLFQ Scheduler")
    queues = {1: [], 2: [], 3: []}
    time_quantums = {1: 5, 2: 10, 3: float('inf')}
    current_time = 0
    results = {pid: {'completion': 0, 'response': 0} for pid in processes}

    for pid, bursts in processes.items():
        queues[1].append((pid, bursts[:]))

    while any(queues.values()):
        for queue_num in [1, 2, 3]:
            if queues[queue_num]:
                pid, bursts = queues[queue_num].pop(0)
                if results[pid]['response'] == 0:
                    results[pid]['response'] = current_time
                cpu_burst = bursts.pop(0)
                tq = time_quantums[queue_num]

                if cpu_burst > tq:
                    current_time += tq
                    cpu_burst -= tq
                    if bursts:
                        queues[min(queue_num + 1, 3)].append((pid, [cpu_burst] + bursts))
                    else:
                        queues[min(queue_num + 1, 3)].append((pid, [cpu_burst]))
                else:
                    current_time += cpu_burst
                    if bursts:
                        queues[queue_num].append((pid, bursts))
                    else:
                        results[pid]['completion'] = current_time

                if not bursts:
                    results[pid]['completion'] = current_time
                break
        else:
            current_time += 1
    show_results("MLFQ", results)



fcfs_scheduler(DATA)
sjf_scheduler(DATA.copy())
mlfq_scheduler(DATA.copy())

