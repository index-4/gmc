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
                if task[0]:  # command must have args (e.g. commit message)
                    tasks.append(Task(task[2], task[1], next(arg_iter)))
                else:
                    tasks.append(Task(task[2], task[1]))
    except StopIteration:  # no more args to parse
        pass
    except KeyError as failed_key:
        print(f"Given argument {failed_key} does not exist!")
        sys.exit()
    except Exception as ex:
        print(ex)
        sys.exit()
    # explicitly add magic add to tasks, if not single command or gmc only
    if len(sys.argv) != 2:
        tasks.insert(0, Task(git_magic_add, 2))
    return tasks


if __name__ == "__main__":
    tasks = parse_args()
    batch = Batch(tasks)
    batch.run()
