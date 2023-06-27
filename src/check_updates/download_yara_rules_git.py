import git

def download_yara_rules_git():
    git.Git().clone("https://github.com/Yara-Rules/rules")