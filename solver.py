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
    global_best_ret = []
    global_best_score = 0
    ntrials = 5
    
    original = tasks.copy()

    for trial in range(ntrials):
        epoch_best_ret = []
        epoch_best_score = 0
        random.shuffle(tasks)
        ret = get_tasks(tasks)

        # Simulating annealing
        temp = 100.0
        nepochs = 10000
        a = 0.999
        

        for epoch in range(nepochs):
            # Do the random part
            i = random.randint(0, len(tasks)-1)
            j = random.randint(0, len(tasks)-1)
            # tasks.insert(i, tasks.pop(j))
            # Swap positions
            tasks[i], tasks[j] = tasks[j], tasks[i]
            ret = get_tasks(tasks)
            new_score = score(ret, original)
            c = new_score - epoch_best_score
            if abs(c) < 0.0001:
                c = 0.0
            if c >= 0:
                epoch_best_score = new_score
                epoch_best_ret = ret
            elif random.uniform(0, 1) < np.exp(c/temp):
                # print("Taking subobtimal in hopes of brighter future:", epoch, "| old best:", epoch_best_score, "|new worse: ", new_score, "| c:", c)
                epoch_best_score = new_score
                epoch_best_ret = ret
            else:
                # tasks.insert(j, tasks.pop(i))
                # Swap back if rejected
                tasks[i], tasks[j] = tasks[j], tasks[i]
            temp *= a
            
            # Swap everything every 10,000 iterations
            if epoch % 20000 == 0 and epoch != 0:
                for i in range(len(tasks)):
                    for j in range(len(tasks)):
                        # Swap positions
                        tasks[i], tasks[j] = tasks[j], tasks[i]
                        ret = get_tasks(tasks)
                        new_score = score(ret, original)
                        c = new_score - epoch_best_score
                        if c >= 0:
                            epoch_best_score = new_score
                            epoch_best_ret = ret
                        else:
                            # Swap back if rejected
                            tasks[i], tasks[j] = tasks[j], tasks[i]
            # Update global maximum if exists
            if global_best_score < epoch_best_score:
                # print(score(epoch_best_ret, original))
                global_best_score = epoch_best_score
                global_best_ret = epoch_best_ret
        print("TRIAL BEST:", epoch_best_score)
    print("GLOBAL BEST:", global_best_score)
    print(global_best_ret)
    return global_best_ret


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
    for input_path in os.listdir('inputs/small/')[:1]:
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

