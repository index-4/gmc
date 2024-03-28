import sys
from gmc_arg_funcs import gmc_args, git_magic_add
from gmc_helper_classes import Task, Batch

# returns a list of runnable tasks
def parse_args() -> list:
    tasks = []
    arg_iter = iter(sys.argv[1:])
    current_index = 1
    try:
        while arg := next(arg_iter):
            if task := gmc_args[arg]:
                if task[0] == 1:  # command must have args (e.g. commit message)
                    try:
                        tasks.append(Task(task[2], task[1], next(arg_iter)))
                        current_index += 1
                    except StopIteration:  # needed args were not given
                        if task[0] == 1:
                            raise Exception(f"Needed args for '{arg}' not given!")
                        else:
                            tasks.append(Task(task[2], task[1], "$d34d$"))
                elif task[0] == 2: # command could have args
                    try:
                        if not gmc_args.is_key_known(sys.argv[current_index + 1]):
                            tasks.append(Task(task[2], task[1], next(arg_iter)))
                            current_index += 1
                        else:
                            tasks.append(Task(task[2], task[1]))
                    except IndexError:
                        tasks.append(Task(task[2], task[1]))
                else:
                    tasks.append(Task(task[2], task[1]))
            current_index += 1
    except StopIteration:  # no more args overall to parse
        pass
    except KeyError as failed_key:
        print(f"Given argument {failed_key} does not exist!")
        sys.exit()
    except Exception as ex:
        print(f"UNKNOWN ERR: {ex}")
        sys.exit()
    # explicitly add magic add to tasks, if not single command or gmc only
    if len(sys.argv) != 2 and all(map(lambda arg: gmc_args.is_key_known(arg), sys.argv[1:])):
        tasks.insert(0, Task(git_magic_add, 2))
    return tasks


if __name__ == "__main__":
    tasks = parse_args()
    batch = Batch(tasks)
    batch.run()