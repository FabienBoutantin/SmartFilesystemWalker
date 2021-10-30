
import os
import sys
import pathlib


def walk(base_dir, ignore_file=".gitignore"):
    for root, dirs, files in os.walk(base_dir):
        pl_root = pathlib.Path(root)
        if ".git" in dirs:
            dirs.remove(".git")
        if ignore_file in files:
            # update ignore list
            pass
        for file in sorted(files):
            if file == ignore_file:
                continue
            yield pl_root / file


def main():
    for f in walk(sys.argv[1]):
        print(str(f).encode("utf-8", errors="replace").decode("utf-8"))
    return 0


if __name__ == "__main__":
    exit(main())
