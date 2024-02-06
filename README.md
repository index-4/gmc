<img src="assets/banner_white.svg" alt="drawing" width="300" />

# gmc - Git Magical Commit
Git wrapper for easy git message formats.

## Usage

### `gmc` only
Invoking the `gmc` command without any args results in a “git magic add”. That is a special feature of gmc which helps with commits if your current working directory is in a subdirectory of your git repo. “git magic add” searches for the root `.git` directory in its parent directories. It can find the .git directory up to 10 parent directories. This behavior can be prevented by adding the `na` command.

### Available commands

```
h | -h | H | --help                       : shows this message; what did you think it would do?
v | -v | V | --version                    : shows gmc version
s | -s | S | --status                     : prints git status
fe | -fe | --feature <feature_dec>        : adds feature description to commit message; for more info about how to write descriptions see gmc confluence
fs | -fs | --feature-start <feature_name> : starts a new git flow feature
fi | -fi | --fix <fix_description>        : adds fix description to commit message; for more info about how to write descriptions see gmc confluence
bs | -bs | --bugfix-start <bugfix_name>   : starts a new git flow bugfix
co | -co | --commit-only <commit_desc>    : only stashes changes and adds commit message
d | -d | --done                           : tells gmc to finish the current feature / bugfix branch (auto detected)
r | -r | --reference <issue_id>           : adds a reference to a GitHub or Jira issue
!r | -!r | --random                       : push to origin with a random commit message from whatthecommit.com
sc | -sc | --store-credentials            : inits the git credential helper process for the local repository
i | -i | I | --init <git_repo_url>        : inits from a fresh git repo and adds git flow structure
p | -p | P | --push                       : tells gmc to push the current state
!p | -!p | !P | --pull                    : tells gmc to pull from origin
na | -na | --no-add                       : advises gmc to drop magic add (basically git add that searches for root git dir)
c | -c | --config | --change-config       : change your gmc config in your preferred editor (per default nano)
m | -m | --multi-pull                     : Pull multiple repositories, in the current directory, at once
b | -b | --branch                         : Prints `git branch` output
ch | -ch | --checkout                     : Short version of `git checkout`
```

### Argument format
| argument | format | tips |  
| ------------- | -------------| --- |  
| fe | “heading(commit name)~scope_desc1-desc2-desc3(describe here what you changed for the feature; descriptions are separated by ‘-'; leading and trailing white spaces get trimmed; if you need ‘-’ or '_’ in your commit message use camel case instead)” |
| fi | “heading(commit name)~scope_reason1-reason2(list here the reasons for the bug; reasons are separated by ‘-'; leading and trailing white spaces get trimmed)_solution1-solution2(list here the solutions that fixed the bug reasons; reasons are separated by '-'; leading and trailing white spaces get trimmed; if you need '-’ or '_’ in your commit message use camel case instead)” |
| co | “heading_desc1-desc2-…” | heading and _ can be omitted. But be warned: “_” and “-” still get parsed. |
| r | “#1(GitHub issue number or Jira issue id)” | |

### Usage
#### Linux
After downloading the binary from the Releases tab in GitHub, move gmc to /usr/local/bin:
```
sudo cp Downloads/gmc /usr/local/bin
```

### azure configuration
1. [install](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli-linux?pivots=apt) azure cli
2. [add devops](https://learn.microsoft.com/en-us/azure/devops/cli/?view=azure-devops):
`az extension add --name azure-devops`
3. add git aliases:
`az devops configure --use-git-aliases true`
