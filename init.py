import os

encoding="utf-8"
dau_path="c:/code"
cwd_path=(os.getcwd().split("\\"))

if cwd_path[-1]=="code":
    repo_name=input("repo_name: ")
    if repo_name:
        os.chdir(f"c:/code/{repo_name}")
    else:
        os.chdir(f"{dau_path}/base")
print(f"current: {os.getcwd()}")