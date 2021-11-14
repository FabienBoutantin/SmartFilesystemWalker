import pathlib
import sys
import functools
import subprocess

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))

import main  # noqa


@functools.lru_cache
def get_test_materials_dir():
    """Returns the path of the test-materials directory."""
    return pathlib.Path(__file__).parent / "test-materials"


def test_simple_ignore():
    """Tests a simple ignore file"""
    test_materials = get_test_materials_dir() / "ignorefiles"
    assert len(tuple(main.walk(test_materials))) == 6


def dtest_ignore_wildcard():
    """Test ignoring files based on wildcards"""
    pass


def dtest_ignore_subdir():
    pass


def test_listing_ignore_files():
    ignored_files = tuple(main.walk(
        get_test_materials_dir() / "ignorefiles",
        list_ignored_only=True
    ))
    assert len(ignored_files)


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

    tool_set = set(main.walk(
        get_test_materials_dir() / "ignorefiles",
        list_ignored=False
    ))
    print("/°\\_"*10)
    first = True
    for f in sorted(git_ignore_set.intersection(tool_set)):
        if first:
            first = False
            print("Files ignored by Git, but reported by tool:")
        print(" *", str(f).encode("utf-8", errors="replace").decode("utf-8"))
    assert first


def test_ignore_mechanism2():
    tool_no_ignore_set = set(main.walk(
        get_test_materials_dir() / "ignorefiles",
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
    assert first
