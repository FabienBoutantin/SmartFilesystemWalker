import os
import subprocess
import pathlib
import shutil
import json


def move_ignore_files():
    for root, dirs, files in os.walk("."):
        ignore_file = pathlib.Path(root) / "gitignore"
        if ignore_file.exists():
            shutil.copy(ignore_file, pathlib.Path(root) / ".gitignore")


def git_init():
    if pathlib.Path(".git").is_dir():
        return True
    output = subprocess.check_output(
        ["git", "init", "."]
    )
    print(output.decode("utf-8"))
    return True


def generate_info_file():
    output = subprocess.check_output(
        ["git", "status", "--porcelain", "--ignored", "--untracked-files"]
    )
    files = {
        "ignored": list(),
        "to_track": list(),
    }
    for line in output.decode("utf-8").splitlines():
        if line.startswith("?? "):
            files["to_track"].append(line[3:].strip())
            continue
        if line.startswith("!! "):
            files["ignored"].append(line[3:].strip())
            continue
        print("Unknown status:", line)
    with open("git_info_file.json", "w", encoding="utf-8") as fd:
        json.dump(files, fd, indent=2)


def cleanup():
    # remove git init stuff
    dot_git = pathlib.Path(".git")
    if dot_git.is_dir():
        shutil.rmtree(dot_git)
    # revert .gitignore files
    for root, dirs, files in os.walk("."):
        ignore_file = pathlib.Path(root) / ".gitignore"
        if ignore_file.exists():
            ignore_file.unlink()
    pass


def generate_git_info_for_ignorefiles():
    os.chdir(pathlib.Path(__file__).parent / "test-materials" / "ignorefiles")
    move_ignore_files()
    git_init()
    generate_info_file()
    cleanup()


if __name__ == "__main__":
    generate_git_info_for_ignorefiles()
