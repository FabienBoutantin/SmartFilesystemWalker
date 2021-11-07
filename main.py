
import os
import pathlib
import re
import subprocess


def read_ignore_file(root, filepath):
    def translate(item):
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
        return result + "$"

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
            # print(line, "==>", translate(line))
            result.append(
                (
                    line_no,
                    orig_line.rstrip(),
                    re.compile(translate(line)),
                    is_negative
                )
            )
    return result


def walk(
    base_dir,
    ignore_file=".gitignore", list_ignored=False, list_ignored_only=False
):
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
            # print("  ", ignore_list)
        for file in sorted(files):
            if file == ignore_file:
                continue
            file_is_ignored = False
            for k in reversed(ignore_list):
                need_break = False
                for line_no, line, line_re, is_negative in reversed(
                    ignore_list[k]
                ):
                    if line_re.match(f"{root}/{file}"):
                        file_is_ignored = not is_negative
                        need_break = True
                        print(
                            f"{k}/{ignore_file}:{line_no}:{line}"
                            " \t "
                            f"{root}/{file}"
                        )
                        break
                if need_break:
                    break
            if file_is_ignored:
                if list_ignored_only or list_ignored:
                    yield pl_root / file
                continue
            if not list_ignored_only:
                yield pl_root / file


def test_ignore_mechanism():
    git_ignore_set = set()
    # Need to investigate if it is working with committed files:
    # may be this command can be more useful:
    # git check-ignore test-materials/ignorefiles/subdir1/* -v
    output = subprocess.check_output(
        ["git", "status", "--ignored", "--porcelain"]
    )
    for line in output.splitlines():
        line = line.decode("utf-8")
        if line.startswith("!!"):
            git_ignore_set.add(pathlib.Path(line[2:].strip()))

    tool_set = set(walk(
        "test-materials/ignorefiles",
        list_ignored=False
    ))
    print("/°\\_"*10)
    first = True
    for f in sorted(git_ignore_set.intersection(tool_set)):
        if first:
            first = False
            print("Files ignored by Git, but reported by tool:")
        print(" *", str(f).encode("utf-8", errors="replace").decode("utf-8"))

    tool_no_ignore_set = set(walk(
        "test-materials/ignorefiles",
        ignore_file=None,
        list_ignored=True,
        list_ignored_only=True
    ))
    print("/°\\_"*10)
    first = True
    for f in sorted(tool_no_ignore_set):
        if first:
            first = False
            print("Files ignored even if no ignore file given:")
        print(" *", str(f).encode("utf-8", errors="replace").decode("utf-8"))

    return 0


def main():
    test_ignore_mechanism()


if __name__ == "__main__":
    exit(main())
