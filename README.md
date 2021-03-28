<img src="assets/banner_white.svg" alt="drawing" width="300" />

# gmc - Git Magical Commit
Git wrapper for easy git message formats.

## Usage

### `gmc` only
Invoking the `gmc` command without any args results in a “git magic add”. That is a special feature of gmc which helps with commits if your current working directory is in a subdirectory of your git repo. “git magic add” searches for the root `.git` directory in its parent directories. It can find the .git directory up to 10 parent directories. This behavior can be prevented by adding the `na` command.

### Available commands

```
h | -h | H | --help                           : shows this message; what did you think it would do?
v | -v | V | --version                    : shows gmcversion
s | -s | S | --status                     : prints gitstatus
fe | -fe | --feature <feature_dec>        : addsfeature description to commit message; for more infoabout how to write descriptions see gmc confluence
fs | -fs | --feature-start <feature_name> : starts anew git flow feature
fi | -fi | --fix <fix_description>        : adds fixdescription to commit message; for more info about howto write descriptions see gmc confluence
bs | -bs | --bugfix-start <bugfix_name>   : starts anew git flow bugfix
co | -co | --commit-only <commit_desc>    : onlystashes changes and adds commit message
d | -d | --done                           : tells gmcto finish the curent feature / bugfix branch (autodetected) and add a changelog-relevant flag
r | -r | --reference <issue_id>           : adds areference to a GitHub or Jira issue
sc | -sc | --store-credentials            : inits thegit credential helper process for the local repository
i | -i | I | --init                       : inits froma fresh git repo and adds git flow structure
p | -p | P | --push                       : tells gmcto push the current state
na | -na | --no-add                       : advises gmcto drop magic add (basically git add that searches forroot git dir)
c | -c | --config | --change-config       : change your gmc config in your preferred editor (per default nano)
```

### Argument format
| argument | format | tips |  
| ------------- | -------------| --- |  
| fe | “heading(commit name)_desc1-desc2-desc3(describe here what you changed for the feature; descriptions are separated by ‘-'; leading and trailing white spaces get trimmed; if you need ‘-’ or '_’ in your commit message use camel case instead)” |
| fi | “heading(commit name)_reason1-reason2(list here the reasons for the bug; reasons are separated by ‘-'; leading and trailing white spaces get trimmed)_solution1-solution2(list here the solutions that fixed the bug reasons; reasons are separated by '-'; leading and trailing white spaces get trimmed; if you need '-’ or '_’ in your commit message use camel case instead)” |
| co | “heading_desc1-desc2-…” | heading and _ can be omitted. But be warned: “_” and “-” still get parsed. |
| r | “#1(GitHub issue number or Jira issue id)” | |