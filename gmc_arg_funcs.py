import os
import sys
from gmc_emojis import Emojis
from gmc_helper_classes import Help, AliasDict, TestMappings
from gmc_config import Config
import urllib.request
from time import sleep


flags: dict[str, str] = {}

execution_path = os.getcwd()
stash_directory = None

def display_help():
    help_message = Help(
        f"Welcome to gmc (Git magic commit)! {Config().content['version']}\nThis is a git commit message formatter that helps with taming the wild wild git commits.",
        [
            (
                ["h", "-h", "H", "--help"],
                "shows this message; what did you think it would do?",
            ),
            (["v", "-v", "V", "--version"], "shows gmc version"),
            (["s", "-s", "S", "--status"], "prints git status"),
            (
                ["fe", "-fe", "--feature <feature_dec>"],
                "adds feature description to commit message; for more info about how to write descriptions see gmc confluence",
            ),
            (
                ["fs", "-fs", "--feature-start <feature_name>"],
                "starts a new git flow feature",
            ),
            (
                ["fi", "-fi", "--fix <fix_description>"],
                "adds fix description to commit message; for more info about how to write descriptions see gmc confluence",
            ),
            (
                ["bs", "-bs", "--bugfix-start <bugfix_name>"],
                "starts a new git flow bugfix",
            ),
            (
                ["co", "-co", "--commit-only <commit_desc>"],
                "only stashes changes and adds commit message",
            ),
            (
                ["d", "-d", "--done"],
                "tells gmc to finish the curent feature / bugfix branch (auto detected) and add a changelog-relevant flag",
            ),
            (
                ["t", "-t", "--test <test_command>"],
                "instructs gmc to test your code befor pushing; either tests via given command or from test mapping in config",
            ),
            (
                ["r", "-r", "--reference <issue_id>"],
                "adds a reference to a GitHub or Jira issue",
            ),
            (
                ["!r", "-!r", "--random"],
                "push to origin with a random commit message from whatthecommit.com",
            ),
            (
                ["sc", "-sc", "--store-credentials"],
                "inits the git credential helper process for the local repository",
            ),
            (
                ["i", "-i", "I", "--init <git_repo_url>"],
                "inits from a fresh git repo and adds git flow structure",
            ),
            (["p", "-p", "P", "--push"], "tells gmc to push the current state"),
            (["!p", "-!p", "!P", "--pull"], "tells gmc to pull from origin"),
            (
                ["na", "-na", "--no-add"],
                "advises gmc to drop magic add (basically git add that searches for root git dir)",
            ),
            (
                ["c", "-c", "--config", "--change-config"],
                "change your gmc config in your preferred editor (per default nano)",
            ),
            (
                ["m", "-m", "--multi-pull"],
                "Pull multiple repositories, in the current directory, at once",
            ),
        ],
    )
    print(help_message)
    sys.exit(0)


def git_push():
    print("Pushing to origin")
    os.system("git push")


def git_pull():
    print("Pulling from origin")
    os.system("git pull")


def traverse_up():
    max_iter = 0  # max out at 10 dirs up
    while not os.path.exists(".git") and max_iter < 10:
        os.chdir("..")
        max_iter += 1
    return max_iter


def git_magic_add(target_directory: str = None):
    if "na" in flags.keys():
        print("Preventing magic add")
        return
    stash_directory = target_directory
    if stash_directory is None:
        max_iter = traverse_up()
        stash_directory = os.getcwd()
        if max_iter == 10:
            print("Couldn't find git repository!")
            sys.exit(-1)
    os.system(f"git add {stash_directory}")
    print(f"Stashed files from directory {stash_directory}")


def check_flags(commit_message: str):
    finish_flow = False

    if "ref" in flags.keys():
        commit_message += f'-m "references {flags["ref"]}" '

    if "done" in flags.keys():
        finish_flow = True

    return finish_flow, commit_message


def execute_tests():
    if "test" in flags.keys():
        if flags["test"]:
            os.system(flags["test"])
        else:
            try:
                os.chdir(execution_path)
                os.system(TestMappings().get_by_relative_path(execution_path))
                traverse_up()
            except KeyError or TypeError:
                print("Directory is not mapped for tests in config and no test command was given!")
                sys.exit(404)
        print("Tests finished if you wanna abort the commit (CTRL + C) due to failed tests I'll give you 5 seconds...")
        try:
            sleep(5)
        except:
            print("Aborting commit due to failed tests")
            sys.exit(0)


def parse_feature(feature_message: str):
    finish_feature = False
    feature_name, changes = feature_message.split("_")
    scope = None
    try:
        feature_name, scope = feature_name.split("~")
    except ValueError:
        pass  # swallow if no scope
    changes = [change.strip() for change in changes.split("-")]

    # build commit message
    message = f'-m "feat{f"({scope})" if scope else ""}: {feature_name} {Emojis.feature}" '  # header
    feature_desc = f'-m "  - {changes[0]}'  # description
    for change in changes[1:]:
        feature_desc += f"{os.linesep}  - {change}"
    message += feature_desc + '" '  # end description

    finish_feature, message = check_flags(message)

    execute_tests()

    os.system(f"git commit {message}")
    if finish_feature:
        if Config().content["public_config"]["default_git_handler"] == "git":
            os.system(f"gh pr create -B develop")
        else:
            project_name = Config().content["public_config"]["azure_project"]
            repo_name = os.getcwd().split("/")[-1]
            work_items = ""
            if "ref" in flags.keys():
                work_items = f"--work-items {flags['ref'].replace('#', '')}"
            os.system(f"git pr create --target-branch develop --project {project_name} --repository {repo_name} {work_items} --squash true --description {message.replace('-m ', '')}")


def parse_feature_start(feature_name: str):
    os.system(f"git flow feature start {feature_name}")
    parse_commit_only(f"initial commit for feature {feature_name}_")
    os.system(f"git push --set-upstream origin feature/{feature_name}")
    sys.exit(0)


def parse_fix(fix_message: str):
    print(fix_message)
    finish_bugfix = False
    fix_name, reasons, solutions = fix_message.split("_")
    scope = None
    try:
        fix_name, scope = fix_name.split("~")
    except ValueError:
        pass # swallow if no scope
    reasons = [reason.strip() for reason in reasons.split("-")]
    solutions = [solution.strip() for solution in solutions.split("-")]

    # build commit message
    message = f'-m "fix{f"({scope})" if scope else ""}: {fix_name} {Emojis.fix}" '  # header
    message += f'-m "  reasons:'  # reasons (also opening quotes)
    for reason in reasons:
        message += f"{os.linesep}    - {reason}"
    message += f"{os.linesep}  solutions:"  # solutions
    for solution in solutions:
        message += f"{os.linesep}    - {solution}"
    message += '" '  # end reasons and solutions

    finish_bugfix, message = check_flags(message)

    execute_tests()

    os.system(f"git commit {message}")
    if finish_bugfix:
        if Config().content["public_config"]["default_git_handler"] == "git":
            os.system(f"gh pr create")
        else:
            project_name = Config().content["public_config"]["azure_project"]
            repo_name = os.getcwd().split("/")[-1]
            work_items = ""
            if "ref" in flags.keys():
                work_items = f"--work-items {flags['ref'].replace('#', '')}"
            os.system(f"git pr create --target-branch develop --project {project_name} --repository {repo_name} {work_items} --squash true --description {message.replace('-m ', '')}")


def parse_fix_start(fix_name: str):
    os.system(f"git flow bugfix start {fix_name}")
    parse_commit_only(f"initial commit for fix {fix_name}_")
    os.system(f"git push --set-upstream origin bugfix/{fix_name}")
    sys.exit(0)


def parse_commit_only(commit_message: str):

    commit_name = None

    try:
        commit_name, changes = commit_message.split("_")
        changes = [change.strip() for change in changes.split("-")]
    except:
        # well looks like one omitted the heading :(
        changes = [change.strip() for change in commit_message.split("-")]

    # remove empty changes
    changes = [change for change in changes if change != ""]

    # admit that someone tried that
    if "done" in flags.keys():
        print("Nice try! Though you can't end a flow in a commit only ;)")

    # build commit message
    if commit_name is not None:
        message = f'-m "{commit_name}" '  # header
        if len(changes) > 0:
            commit_desc = f'-m "  - {changes[0]}'  # description
            for change in changes[1:]:
                commit_desc += f"{os.linesep}  - {change}"
            message += commit_desc + '" '  # end description
    else:  # omitted header
        message = '-m "intermediate commit" '  # header
        if len(changes) > 0:
            message += f'-m "- {changes[0]}'  # description
            for change in changes[1:]:
                message += f"{os.linesep}- {change}"
            message += '" '  # end description

    _, message = check_flags(message)

    execute_tests()

    os.system(f"git commit {message}")


def parse_store_credentials():
    os.system("git config credential.helper store")
    os.system("git pull")


def git_init(git_url: str):
    print(f"creating git repo for {git_url}")
    with open("README.md", "w") as readme:
        readme.write(f"# {os.path.basename(os.getcwd())}")
    os.system("git init")
    git_magic_add(".")
    parse_commit_only("initial commit_added README")
    os.system("git branch -M master")
    os.system(f"git remote add origin {git_url}")
    os.system("git push -u origin master")
    os.system("git flow init -d")
    os.system("git checkout develop")
    os.system("git push --set-upstream origin develop")


# just in case ¯\_(ツ)_/¯
def git_status():
    os.system("git status")


def multi_pull():
    os.system("find . -mindepth 1 -maxdepth 1 -type d -print -exec git -C {} pull \\;")


def git_random_commit():
    quote = urllib.request.urlopen("http://whatthecommit.com/index.txt").read().decode() + "_"
    git_magic_add()
    parse_commit_only(quote)
    os.system("git push")


# stores functions that shall be executed by gmc; format (needs_args, prio, function)
# needs_args: in range [0,2] -> [no, yes, optional]
# prios (from high to low): 4 3 [2] 1 0; 2 is default
gmc_args = AliasDict(
    {
        "h": (0, 4, display_help),
        "v": (0, 4, lambda: print(Config().content["version"])),
        "p": (0, 0, git_push),
        "!p": (0, 0, git_pull),
        "s": (0, 0, git_status),
        "a": (0, 2, git_magic_add),
        "na": (0, 3, lambda: flags.update({"na": None})),
        "fi": (1, 1, parse_fix),
        "fe": (1, 1, parse_feature),
        "fs": (1, 3, parse_feature_start),
        "bs": (1, 3, parse_fix_start),
        "co": (1, 1, parse_commit_only),
        "sc": (0, 0, parse_store_credentials),
        "i": (1, 4, git_init),
        "t": (2, 2, lambda command=None: flags.update({"test": command})),
        "r": (1, 2, lambda ref: flags.update({"ref": ref})),
        "!r": (0, 0, git_random_commit),
        "d": (0, 2, lambda: flags.update({"done": None})),
        "c": (0, 0, lambda: Config().edit()),
        "m": (0, 0, multi_pull),
    },
    aliases={
        # help aliases
        "-h": "h",
        "H": "h",
        "--help": "h",
        # version aliases
        "-v": "v",
        "V": "v",
        "--version": "v",
        # push aliases
        "P": "p",
        "-p": "p",
        "--push": "p",
        # pull aliases
        "!P": "!p",
        "-!p": "!p",
        "--pull": "!p",
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
        # fix start aliases
        "-bs": "bs",
        "--bugfix-start": "bs",
        # feature aliases
        "-fe": "fe",
        "--feature": "fe",
        # feature start aliases
        "-fs": "fs",
        "--feature-start": "fs",
        # commit only aliases
        "-co": "co",
        "--commit-only": "co",
        # store credentials aliases
        "-sc": "sc",
        "--store-credentials": "sc",
        # init aliases
        "-i": "i",
        "I": "i",
        "--init": "i",
        # test aliases
        "-t": "t",
        "--test": "t",
        # reference aliases
        "-r": "r",
        "--reference": "r",
        # random aliases
        "-!r": "!r",
        "--random": "!r",
        # done aliases
        "-d": "d",
        "--done": "d",
        # config aliases
        "-c": "c",
        "--config": "c",
        "--change-config": "c",
        # multi-pull aliases
        "-m": "m",
        "--multi-pull": "m",
    },
)
