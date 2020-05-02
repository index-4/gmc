import os
import sys

class AliasDict(dict):

    def __init__(self, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)
        self.aliases = kwargs.get("aliases") if kwargs.get("aliases") is not None else {}

    def __getitem__(self, key):
        return dict.__getitem__(self, self.aliases.get(key, key))

    def __setitem__(self, key, value):
        return dict.__setitem__(self, self.aliases.get(key, key), value)

    def add_alias(self, key, alias):
        self.aliases[alias] = key


flags = []


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
    if "na" in flags:
        print("Preventing magic add")
        return
    stash_directory = target_directory
    if stash_directory is None:
        max_iter = 0 # max out at 10 dirs up 
        while not os.path.exists(".git") and max_iter < 10:
            os.chdir("..")
            max_iter += 1
        stash_directory = os.getcwd()
        if max_iter == 10:
            print("Couldn't find git repository!")
            sys.exit(-1)
    os.system(f"git add {stash_directory}")
    print(f"Stashed files from directory {stash_directory}")


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
        "na": (False, 3, lambda: flags.append("na")),
        "f": (True, 1, "kuchen")
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
    }
)