#! env/python3

from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent))

import _main  # noqa


__all__ = []

walk = _main.walk  # noqa