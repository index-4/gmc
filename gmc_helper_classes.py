from gmc_config import Config
from art import text2art

# most important custom command imports (keep 'em)
import os
import sys
import yaml


class Task:
    def __init__(self, runnable, prio, *args):
        self._runnable = runnable
        self.prio = prio
        self._args = " ".join(args) if len(args) != 0 else None

    def run(self):
        if self._args:
            if "$d34d$" in self._args:
                self._runnable("")
            else:
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
        self._tasks = sorted(self._tasks, key=lambda task: task.prio, reverse=True)
        for task in self._tasks:
            task.run()


class AliasDict(dict):
    def __init__(self, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)
        self.aliases = (
            kwargs.get("aliases") if kwargs.get("aliases") is not None else {}
        )
        self.infuse_custom_commands()

    def __getitem__(self, key):
        return dict.__getitem__(self, self.aliases.get(key, key))

    def __setitem__(self, key, value):
        return dict.__setitem__(self, self.aliases.get(key, key), value)

    def add_alias(self, key, alias):
        self.aliases[alias] = key

    def is_key_known(self, key: str):
        return key in self.aliases.keys() or key in self.keys()

    def infuse_custom_commands(self):
        for command in Config().content["public_config"]["custom_commands"]:
            command_name = list(command.keys())[0]
            needs_args = 0
            priority = 0

            try:
                needs_args = command[command_name]["needs_args"]
                if needs_args < 0 or needs_args > 2:
                    raise ValueError(
                        f"Needs args must be in [0,2]; check your config for command '{command_name}'"
                    )
            except KeyError:
                pass
            try:
                priority = command[command_name]["priority"]
            except KeyError:
                pass

            self.update(
                {
                    command[command_name]["args"][0]: (
                        needs_args,
                        priority,
                        (
                            lambda call_args=None, command=command[command_name][
                                "exec"
                            ]: exec(command, None, {"call_args": call_args})
                        ),
                    )
                }
            )
            for arg in command[command_name]["args"][1:]:
                self.add_alias(command[command_name]["args"][0], arg)


class TestMappings:

    mappings = {}

    def __init__(self):
        for mapping in Config().content["public_config"]["test_mappings"]:
            self.mappings.update(mapping)

    def get_by_relative_path(self, path: str):
        for key in self.mappings:
            if key in path:
                return self.mappings[key]


class Help:
    def __init__(self, description: str, options_n_descs: list):
        """options should be a list of tuples; containing option (can also be list of options) and according description"""
        self.description = description
        self.options_n_descs = options_n_descs
        for command in Config().content["public_config"]["custom_commands"]:
            command_name = list(command.keys())[0]
            help_msg = "Non given :("
            show_command = True

            try:
                help_msg = command[command_name]["help"]
            except KeyError:
                pass
            try:
                show_command = command[command_name]["show_in_help"]
            except KeyError:
                pass

            if not show_command:
                continue
            self.options_n_descs.append((command[command_name]["args"], help_msg))

    def __repr__(self):
        return (
            f"{text2art('gmc')}\n{self.description}\n\nOptions:\n{self.parse_options()}"
        )

    def parse_options(self):
        options = "    "  # start padding

        # determine longest option for option padding
        longest_option = 0
        for option in self.options_n_descs:
            if len(o_str := " | ".join(option[0])) > longest_option:
                longest_option = len(o_str)

        for option_n_desc in self.options_n_descs:
            if len(option_str := " | ".join(option_n_desc[0])) < longest_option:
                # add end padding
                option_str += " " * (longest_option - len(option_str))
            options += option_str + f" : {option_n_desc[1]}\n    "
        return options
