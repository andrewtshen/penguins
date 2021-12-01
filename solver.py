from parse import read_input_file, write_output_file
import os
import numpy as np

def solve(tasks):
    """
    Args:
        tasks: list[Task], list of igloos to polish
    Returns:
        output: list of igloos in order of polishing  
    """
    best_ret = []
    best_score = 0
    
    for benefit_weight in range(1, 100):
        for deadline_weight in range(500, 2000):
            original = tasks.copy() 
            tasks.sort(key=lambda task: benefit_weight * task.get_max_benefit() + deadline_weight - task.get_deadline() + 60 - task.get_duration(), reverse=True)

            # for task in tasks:
                # print("Task:", task.get_task_id(), "| Deadline: ", task.get_deadline(), "| Duration:", task.get_duration(), "| Benefit:", task.get_max_benefit())
                # High benefit better, sooner deadline better, low duration better
                # print(2 * task.get_max_benefit() + 1440 - task.get_deadline() + 60 - task.get_duration())

            # Start picking tasks
            total_duration = 0
            task_index = 0
            ret = []
            while(task_index != len(tasks) and total_duration + tasks[task_index].get_duration() <= 1440):
                total_duration += tasks[task_index].get_duration()
                ret.append(tasks[task_index].get_task_id())
                task_index += 1

            new_score = score(ret, original)
            if best_score < new_score:
                print(benefit_weight, best_score)
                best_score = new_score
                best_ret = ret
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

