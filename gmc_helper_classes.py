import yaml

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


class Help:

    def __init__(self, description: str, options_n_descs: list):
        """options should be a list of tuples; containing option (can also be list of options) and according description"""
        self.description = description
        self.options_n_descs = options_n_descs

    def __repr__(self):
        return f"{self.description}\n\nOptions:\n{self.parse_options()}"

    @staticmethod
    def version():
        with open("./config.yaml", "r") as config_file:
            return yaml.safe_load(config_file)["version"]

    def parse_options(self):
        options = "    "  # start padding

        # determine longest option for option padding
        longest_option = 0
        for option in self.options_n_descs:
            if len(o_str := " | ".join(option[0])) > longest_option:
                longest_option = len(o_str)
        
        for option_n_desc in self.options_n_descs:
            if len(option_str := " | ".join(option_n_desc[0])) < longest_option:
                option_str += " " * (longest_option - len(option_str))  # add end padding
            options += option_str + f" : {option_n_desc[1]}\n    "
        return options