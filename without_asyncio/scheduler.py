from collections import deque
from main import async_search, lucas, is_prime, async_print_matches


# 3) Define a simple wrapper for coroutine/generator (keep track of id as well)
class Task:
    next_id = 0

    def __init__(self, routine):
        self.id = self.__class__.next_id
        self.__class__.next_id += 1
        self.routine = routine


# 4) Define a simple scheduler
class Scheduler:
    def __init__(self):
        self.runnable_tasks = deque()
        self.completed_tasks_results = {}
        self.failed_tasks_errors = {}

    def add(self, routine):
        task = Task(routine)
        self.runnable_tasks.append(task)
        return task.id

    def run_to_completion(self):
        while self.runnable_tasks:
            task = self.runnable_tasks.popleft()
            print('Running task {} ... '.format(task.id), end='')
            try:
                yielded = next(task.routine)
            except StopIteration as stopped:  # task is finished, save result
                value = stopped.value
                print('Completed with result: {}'.format(value))
                self.completed_tasks_results[task.id] = value
            except Exception as e:  # task is failed, save result
                print('Failed with exception: {}'.format(e))
                self.failed_tasks_errors[task.id] = e
            else:
                assert yielded is None  # yielded was successful
                print('now yielded')
                self.runnable_tasks.append(task)  # add to the back of queue


if __name__ == '__main__':
    scheduler = Scheduler()
    scheduler.add(async_search(lucas(), lambda x: len(str(x)) >= 6))
    scheduler.run_to_completion()
    # >>> Running task 0 ... now yielded
    # >>> Running task 0 ... now yielded
    # >>> Running task 0 ... now yielded
    # >>> Running task 0 ... now yielded
    # >>> Running task 0 ... Completed with result: 103682
    scheduler.completed_tasks_results.pop(0)
    # >>> 103682

    scheduler.add(async_search(lucas(), lambda x: len(str(x)) >= 7))
    scheduler.add(async_search(lucas(), lambda x: len(str(x)) >= 9))
    scheduler.run_to_completion()
    # >>> Running task 1 ... now yielded
    # >>> Running task 0 ... now yielded
    # >>> Running task 1 ... now yielded
    # >>> Running task 0 ... Completed with result: 1149851
    # >>> Running task 1 ... now yielded
    # >>> Running task 1 ... now yielded
    # >>> Running task 1 ... Completed with result: 141422324

    scheduler.add(async_print_matches(lucas(), is_prime))  # >>> 0
    scheduler.run_to_completion()
    # >>> Running task 0 ... Found:  2, now yielded
    # >>> Running task 0 ... now yielded
    # >>> Running task 0 ... Found:  3, now yielded
    # >>> Running task 0 ... now yielded
    # >>> Running task 0 ... Found:  7, now yielded
    # >>> Running task 0 ... Found:  11, now yielded
    # >>> Running task 0 ... now yielded
    # >>> Running task 0 ... Found:  29, now yielded
    # >>> Running task 0 ... Found:  47, now yielded
    # >>> Running task 0 ... now yielded
    # >>> Running task 0 ... now yielded
    # >>> Running task 0 ... Found:  199, now yielded
    # >>> Running task 0 ... now yielded
    # >>> Running task 0 ... Found:  521, now yielded
