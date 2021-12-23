# SmartFilesystemWalker
Walks in a filesystem with automatic configuration generation for current level

The aim is to provide a flexible way to walk through a filesystem, and parsing configuration files (for instance, like git does for .gitignore).

## Developing

## Testing

This module uses pytest with those modules enabled:

- doctest
- flake8 (pep8 compliancy)
- code coverage

Pytests are located in `tests` directory.

To run all those tests, simply run this command:

"""bash
pytest-3
"""

This will print the result in the terminal and the coverage will be available in `htmlcov/index.html`.