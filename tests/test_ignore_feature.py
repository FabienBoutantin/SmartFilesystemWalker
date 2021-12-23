import pathlib
import sys
import functools
import json

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent.parent))

import SmartFilesystemWalker  # noqa: E402


################################################################################
# Helper functions
@functools.lru_cache
def get_test_materials_dir():
    """Returns the path of the test-materials directory."""
    return pathlib.Path(__file__).parent / "test-materials"


@functools.lru_cache
def get_git_info():
    """ Imports last git exported status
    One may need to run this command to update file:
    $> generate_git_info_for_ignorefiles.py
    """
    ignorefiles_dir = get_test_materials_dir() / "ignorefiles"
    with open(ignorefiles_dir / "git_info_file.json", "r", encoding="utf-8") as fd:
        return json.load(fd)


################################################################################
# Tests:

def test_listing_ignore_files():
    # Using default filename that is .gitignore
    ignored_files = tuple(SmartFilesystemWalker.walk(
        get_test_materials_dir() / "ignorefiles",
        list_ignored_only=True
    ))
    # No .gitignore file, hence no ignored files
    assert len(ignored_files) == 0

    ignored_files = tuple(SmartFilesystemWalker.walk(
        get_test_materials_dir() / "ignorefiles",
        ignore_file="gitignore",
        list_ignored_only=True
    ))
    # THere should be more than 1 ignored file
    assert len(ignored_files)


def test_ignore_mechanism():
    ignorefiles_dir = get_test_materials_dir() / "ignorefiles"
    git_ignore_set = set(
        map(
            lambda f: ignorefiles_dir / f,
            filter(
                lambda x: not x.endswith("gitignore"),
                get_git_info()["ignored"]
            )
        )
    )

    tool_set = set(
        map(
            lambda f: ignorefiles_dir / f,
            SmartFilesystemWalker.walk(
                ignorefiles_dir,
                ignore_file="gitignore",
                list_ignored=False
            )
        )
    )

    first = True
    for f in sorted(tool_set.intersection(git_ignore_set)):
        if first:
            first = False
            print("Files ignored by Git, but reported by tool:")
        print(" *", str(f).encode("utf-8", errors="replace").decode("utf-8"))
    if not first:
        print("Reported files by tool:")
        for f in sorted(tool_set):
            print(f)
    assert first


def test_ignored_files():
    ignorefiles_dir = get_test_materials_dir() / "ignorefiles"
    git_to_track_set = set(
        map(
            lambda f: ignorefiles_dir / f,
            filter(
                lambda x: not x.endswith("gitignore"),
                get_git_info()["to_track"]
            )
        )
    )

    tool_set = set(
        map(
            lambda f: ignorefiles_dir / f,
            SmartFilesystemWalker.walk(
                ignorefiles_dir,
                ignore_file="gitignore",
                list_ignored=False
            )
        )
    )
    first = True
    for f in sorted(git_to_track_set.difference(tool_set)):
        if first:
            first = False
            print("Files tracked by Git, but not reported by tool:")
        print(" *", str(f).encode("utf-8", errors="replace").decode("utf-8"))
    assert first
    first = True
    for f in sorted(tool_set.difference(git_to_track_set)):
        if first:
            first = False
            print("Files reported by tool, but not tracked by git:")
        print(" *", str(f).encode("utf-8", errors="replace").decode("utf-8"))
    assert first
