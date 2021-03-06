#! env/python3

from enum import Enum, auto  # noqa: F401
from typing import Union


class Policy(Enum):
    """Policy to use while handling  configuration file.
    Possible values:
    - Override: Last file in hierarchy is the new configuration
    - Concatenate:  Append each found configuration file content
    - DictBased: Dictionary based configuration, but values are immutable
    - DictBasedOverride: Dictionary based, value is the last found one
    - DictBasedAppend: Dictionary based, value is the result of "old + new" values
    - GitIgnoreLike: like .gitignore
    """
    Override = auto()
    Concatenate = auto()
    DictBased = auto()
    DictBasedOverride = auto()
    DictBasedAppend = auto()
    GitIgnoreLike = auto()


def handle_config_file(base_content: Union[str, dict], new_content: Union[str, dict], policy: Policy) -> Union[str, dict]:
    """[summary]

    Args:
        base_content (Union[str, dict]): [description]
        new_content (Union[str, dict]): [description]
        policy (Policy): [description]

    Returns:
        Union[str, dict]: [description]

    >>> handle_config_file("a=12", "b=3", Policy["Override"])
    'b=3'

    >>> handle_config_file("a=12", "b=3", Policy["Concatenate"]).splitlines()
    ['a=12', 'b=3']

    >>> handle_config_file({'a': 12, 'b': 12}, {'b': 3, 'c': 4}, Policy["DictBased"])
    {'a': 12, 'b': 12, 'c': 4}

    >>> handle_config_file({'a': 12, 'b': 12}, {'b': 3, 'c': 4}, Policy["DictBasedOverride"])
    {'a': 12, 'b': 3, 'c': 4}

    >>> handle_config_file({'a': 12, 'b': 12}, {'b': 3, 'c': 4}, Policy["DictBasedAppend"])
    {'a': 12, 'b': 15, 'c': 4}
    >>> handle_config_file({'a': 12, 'b': [12, ]}, {'b': [3, ], 'c': 4}, Policy["DictBasedAppend"])
    {'a': 12, 'b': [12, 3], 'c': 4}

    # WIP: need to move code from _main.py
    >>> handle_config_file("", "", Policy["GitIgnoreLike"])
    Traceback (most recent call last):
    ...
    NotImplementedError: To Be Copied from main code

    # Unknown policy will raise a TypeError
    >>> handle_config_file("a=12", "b=3", "toto")
    Traceback (most recent call last):
    ...
    ValueError: Unknown policy 'toto'
    """
    if policy == Policy["Override"]:
        return new_content
    elif policy == Policy["Concatenate"]:
        return base_content + "\n" + new_content
    elif policy == Policy["DictBased"]:
        result = dict(base_content)
        for k in new_content:
            if k in result:
                continue
            result[k] = new_content[k]
        return result
    elif policy == Policy["DictBasedOverride"]:
        result = dict(base_content)
        result.update(new_content)
        return result
    elif policy == Policy["DictBasedAppend"]:
        result = dict(base_content)
        for k in new_content:
            if k in result:
                result[k] += new_content[k]
            else:
                result[k] = new_content[k]
        return result
    elif policy == Policy["GitIgnoreLike"]:
        raise NotImplementedError("To Be Copied from main code")
    raise ValueError(f"Unknown policy '{policy}'")
