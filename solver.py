from parse import read_input_file, write_output_file
import os
import numpy as np
import random

def solve(tasks):
    """
    Args:
        tasks: list[Task], list of igloos to polish
    Returns:
        output: list of igloos in order of polishing  
    """
    best_ret = []
    best_score = 0
    
    original = tasks.copy() 
    tasks.sort(key=lambda task: 2 * task.get_max_benefit() + 1440 - task.get_deadline() + 60 - task.get_duration(), reverse=True)

    # for task in tasks:
        # print("Task:", task.get_task_id(), "| Deadline: ", task.get_deadline(), "| Duration:", task.get_duration(), "| Benefit:", task.get_max_benefit())
    # Simulating annealing
    temp = 20.0
    nepochs = 100000
    a = 0.999

    for epoch in range(nepochs):
        i = random.randint(0, len(tasks)-1)
        j = random.randint(0, len(tasks)-1)
        # Swap positions
        tasks[i], tasks[j] = tasks[j], tasks[i]
        ret = get_tasks(tasks)
        new_score = score(ret, original)
        # print(new_score)
        c = new_score - best_score
        if c > 0 or random.uniform(0, 1) < np.exp(c/temp):
            # print(epoch, best_score)
            best_score = new_score
            best_ret = ret
        else:
            # Swap back if rejected
            tasks[i], tasks[j] = tasks[j], tasks[i]
        temp *= a
    print(score(best_ret, original))
    return best_ret


def score(arr, tasks):
    total_score = 0.0
    curr_time = 0
    for i in arr:
        task = tasks[i-1]
        curr_time += task.get_duration()
        if curr_time > task.get_deadline():
            total_score += task.get_max_benefit() * np.exp(-0.0170 * (curr_time - task.get_deadline()))
        else:
            total_score += task.get_max_benefit()
    return total_score

def get_tasks(tasks):
# Start picking tasks
    total_duration = 0
    task_index = 0
    ret = []
    while(task_index != len(tasks) and total_duration + tasks[task_index].get_duration() <= 1440):
        total_duration += tasks[task_index].get_duration()
        ret.append(tasks[task_index].get_task_id())
        task_index += 1

    return ret

        


# Here's an example of how to run your solver.
if __name__ == '__main__':
    for input_path in os.listdir('inputs/small/')[:3]:
        print(input_path)
        output_path = 'outputs/small/' + input_path[:-3] + '.out'
        print(output_path)
        tasks = read_input_file('inputs/small/' + input_path)
        output = solve(tasks)
        write_output_file(output_path, output)

    # for input_path in os.listdir('inputs/medium/'):
        # print(input_path)
        # output_path = 'outputs/medium/' + input_path[:-3] + '.out'
        # print(output_path)
        # tasks = read_input_file('inputs/medium/' + input_path)
        # output = solve(tasks)
        # write_output_file(output_path, output)

    # for input_path in os.listdir('inputs/large/'):
        # print(input_path)
        # output_path = 'outputs/large/' + input_path[:-3] + '.out'
        # print(output_path)
        # tasks = read_input_file('inputs/large/' + input_path)
        # output = solve(tasks)
        # write_output_file(output_path, output)

