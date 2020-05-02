import sys
from gmc_arg_funcs import gmc_args, git_magic_add
from gmc_helper_classes import *


# returns a list of runnable tasks
def parse_args() -> list:
    tasks = []
    arg_iter = iter(sys.argv[1:])
    try:
        while arg := next(arg_iter):
            if (task := gmc_args[arg]) is not None:
                if task[0]:  # must have args
                    tasks.append(Task(task[2], task[1], next(arg_iter)))
                else:
                    tasks.append(Task(task[2], task[1]))
    except StopIteration:  # no more args to parse
        pass
    except Exception as ex:
        print(ex)
    # explicitly add magic add to tasks
    tasks.insert(0, Task(git_magic_add, 2))
    return tasks


if __name__ == "__main__":
    tasks = parse_args()
    batch = Batch(tasks)
    batch.run()
