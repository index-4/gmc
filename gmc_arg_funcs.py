import os
import sys


class AliasDict(dict):

    def __init__(self, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)
        self.aliases = kwargs.get("aliases") if kwargs.get(
            "aliases") is not None else {}

    def __getitem__(self, key):
        return dict.__getitem__(self, self.aliases.get(key, key))

    def __setitem__(self, key, value):
        return dict.__setitem__(self, self.aliases.get(key, key), value)

    def add_alias(self, key, alias):
        self.aliases[alias] = key


flags = {}


def display_help():
    print("Welcome to gmc (Git magic commit)!")
    print("This is our git commit message formater that helps us with taming the wild wild git commits.\n")
    print("Available arguments:")
    print("  [h | -h | H | --help]   : shows this message")
    print("  [s | -s | S | --status] : print git status")
    print("  [p | -p | P | --push]   : tells gmc to push the current state")
    print("  [na | -na | --no-add]   : advises gmc to drop magic add (basicly git add that searches for root git dir)")
    sys.exit(0)


def git_push():
    print("Pushing to origin")
    os.system("git push")


def git_magic_add(target_directory: str = None):
    if "na" in flags.keys():
        print("Preventing magic add")
        return
    stash_directory = target_directory
    if stash_directory is None:
        max_iter = 0  # max out at 10 dirs up
        while not os.path.exists(".git") and max_iter < 10:
            os.chdir("..")
            max_iter += 1
        stash_directory = os.getcwd()
        if max_iter == 10:
            print("Couldn't find git repository!")
            sys.exit(-1)
    os.system(f"git add {stash_directory}")
    print(f"Stashed files from directory {stash_directory}")


def parse_feature(feature_message: str):
    feature_name, changes = feature_message.split("_")
    changes = [change.strip() for change in changes.split("-")]

    # build commit message
    message = f'-m "feature {feature_name}:" '  # header
    feature_desc = f'-m "  - {changes[0]}'  # description
    for change in changes[1:]:
        feature_desc += f"{os.linesep}  - {change}"
    message += feature_desc + '" '  # end description

    if "ref" in flags.keys():
        message += f'-m "references {flags["ref"]}" '

    if "done" in flags.keys():
        message += f'-m "changelog-relevant" '
        finish_feature = True

    os.system(f"git commit {message}")
    if finish_feature:
        os.system(f"git flow feature finish")


def parse_fix(fix_message: str):
    fix_name, reasons, solutions = fix_message.split("_")
    reasons = [reason.strip() for reason in reasons.split("-")]
    solutions = [solution.strip() for solution in solutions.split("-")]

    # build commit message
    message = f'-m "fix for {fix_name}:" '  # header
    message += f'-m "  reasons:'  # reasons (also opening quotes)
    for reason in reasons:
        message += f'{os.linesep}    - {reason}'
    message += f'{os.linesep}  solutions:'  # solutions
    for solution in solutions:
        message += f'{os.linesep}    - {solution}'
    message += '" '  # end reasons and solutions

    if "ref" in flags.keys():
        message += f'-m "references {flags["ref"]}" '

    if "done" in flags.keys():
        message += f'-m "changelog-relevant" '
        finish_bugfix = True

    os.system(f"git commit {message}")
    if finish_bugfix:
        os.system("git flow bugfix finish")


# just in case ¯\_(ツ)_/¯
def git_status():
    os.system("git status")


# stores functions that shall be executed by gmc; format (needs_args, prio, function)
# prios (from high to low): 4 3 [2] 1 0; 2 is default
gmc_args = AliasDict(
    {
        "h": (False, 4, display_help),
        "p": (False, 0, git_push),
        "s": (False, 0, git_status),
        "a": (True, 2, git_magic_add),
        "na": (False, 3, lambda: flags.update({"na": None})),
        "fi": (True, 1, parse_fix),
        "fe": (True, 1, parse_feature),
        "r": (True, 2, lambda ref: flags.update({"ref": ref})),
        "d": (False, 2, lambda: flags.update({"done": None}))
    },
    aliases={
        # help aliases
        "-h": "h",
        "H": "h",
        "--help": "h",
        # push aliases
        "P": "p",
        "-p": "p",
        "--push": "p",
        # no add aliases
        "-na": "na",
        "--no-add": "na",
        # status aliases
        "-s": "s",
        "S": "s",
        "--status": "s",
        # fix aliases
        "-fi": "fi",
        "--fix": "fi",
        # feature aliases
        "-fe": "fe",
        "--feature": "fe",
        # reference aliases
        "-r": "r",
        "--reference": "r",
        # done aliases
        "-d": "d",
        "--done": "d",
    }
)
