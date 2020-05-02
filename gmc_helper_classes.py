class Task:

    def __init__(self, runnable, prio, *args):
        self._runnable = runnable
        self.prio = prio
        self._args = " ".join(args) if len(args) != 0 else None

    def run(self):
        if self._args is not None:
            self._runnable(self._args)
        else:
            self._runnable()


class Batch:

    _tasks = []

    def __init__(self, tasks: list):
        self._tasks.extend(tasks)

    def add_task(self, task: Task):
        self._tasks.append(task)

    def run(self):
        # sort by prio -> exec higher prioritised tasks first
        self._tasks = sorted(
            self._tasks, key=lambda task: task.prio, reverse=True)
        for task in self._tasks:
            task.run()
