
import os
import pathlib
import re
from enum import Enum


DEBUG = 1


class ConfigFilePolicy(Enum):
    """Policy to use while handling  configuration file.
    Possible values:
    - Override: Last file in hierarchy is the new configuration
    - Concatenate:  Append each found configuration file content
    - DictBased: Dictionary based configuration, value is the last found one
    - AppendDictBased: Dictionary based, but values are imutable
    - GitIgnoreLike: like .gitignore
    """
    Override = 1
    Concatenate = 2
    DictBased = 4
    AppendDictBased = 8
    GitIgnoreLike = 16


def convert_ignore_line_to_re(item, root):
    """ Converts an ignore line directive into a compiled regex.
    """
    result = "^.*/"
    if item.startswith("**/"):
        result = f"^{root}(|.*)/"
        item = item[3:]
    elif item.startswith("*/"):
        result = f"^{root}/[^/]*/"
        item = item[2:]
    result += ".*".join([
        i.replace("*", "[^/]*")
        for i in item.split("**")
    ])
    if result[-1] != "/":
        result += "$"
    return re.compile(result)


def read_ignore_file(root, filepath):
    """ Reads a ignore file like .gitignore.
    Returns a list of rules according to ignore file content.
    Each rule is a tuple composed of:
    * line number in file
    * original rule text
    * compile regexp of the rule
    * is the rule negative (starts with a '!' char)
    """
    result = list()
    with open(filepath, "rt", encoding="utf-8") as fd:
        for line_no, orig_line in enumerate(fd, 1):
            # remove comments
            line = orig_line.split("#", 1)[0].strip()
            if line == "":
                continue
            if line.startswith("!"):
                is_negative = True
                line = line[1:]
            else:
                is_negative = False
            result.append(
                (
                    line_no,
                    orig_line.rstrip(),
                    convert_ignore_line_to_re(line, root),
                    is_negative
                )
            )
    return result


def is_ignored_item(ignore_rules, item, ignore_file):
    """ Tells if given item must be ignored or not.
    """
    for k in reversed(ignore_rules):
        for line_no, line, line_re, is_negative in reversed(
            ignore_rules[k]
        ):
            if line_re.match(item):
                if DEBUG:
                    print(
                        f"{k}/{ignore_file}:{line_no}:{line}"
                        " \t "
                        f"{item}"
                    )
                return not is_negative
    return False


def walk(
    base_dir,
    ignore_file=".gitignore", list_ignored=False, list_ignored_only=False
):
    if list_ignored_only:
        list_ignored = True
    ignore_list = dict()
    for root, dirs, files in os.walk(base_dir):
        pl_root = pathlib.Path(root)
        for d in (".git", ".svn", ".bzr"):
            if d in dirs:
                dirs.remove(d)
        dirs.sort()
        ignore_list = {
            k: ignore_list[k]
            for k in ignore_list
            if root.startswith(k)
        }
        if ignore_file in files:
            # update ignore list
            ignore_list[root] = read_ignore_file(root, pl_root / ignore_file)
            if DEBUG:
                print("  ", ignore_list)
        for file in sorted(files):
            if file == ignore_file:
                continue
            file_is_ignored = is_ignored_item(
                ignore_list,
                f"{root}/{file}",
                ignore_file
            )
            if file_is_ignored:
                if list_ignored:
                    yield pl_root / file
                continue
            if not list_ignored_only:
                yield pl_root / file
        if not list_ignored:
            # need to prevent walking inside excluded directories for perf.
            ignored_dirs = [
                d
                for d in dirs
                if is_ignored_item(ignore_list, f"{root}/{d}/", ignore_file)
            ]
            for d in ignored_dirs:
                dirs.remove(d)


def main():
    print("This cannot be launched like a script yet")


if __name__ == "__main__":
    exit(main())
