#! env/python3

from enum import Enum, auto  # noqa: F401
from typing import Union


class Policy(Enum):
    """Policy to use while handling  configuration file.
    Possible values:
    - Override: Last file in hierarchy is the new configuration
    - Concatenate:  Append each found configuration file content
    - DictBased: Dictionary based configuration, value is the last found one
    - AppendDictBased: Dictionary based, but values are immutable
    - GitIgnoreLike: like .gitignore
    """
    Override = auto()
    Concatenate = auto()
    DictBased = auto()
    AppendDictBased = auto()
    GitIgnoreLike = auto()


def handle_config_file(base_content: Union[str, dict], new_content: Union[str, dict], policy: Policy) -> Union[str, dict]:
    """[summary]

    Args:
        base_content (Union[str, dict]): [description]
        new_content (Union[str, dict]): [description]
        policy (Policy): [description]

    Returns:
        Union[str, dict]: [description]
    """
    if policy == Policy["Override"]:
        return new_content
    elif policy == Policy["Concatenate"]:
        return base_content + "\n" + new_content
    elif policy == Policy["DictBased"]:
        result = dict(base_content)
        result.update(new_content)
        return result
    elif policy == Policy["AppendDictBased"]:
        result = dict(new_content)
        result.update(base_content)
        return result
    elif policy == Policy["GitIgnoreLike"]:
        raise NotImplementedError("To Be Copied from main code")
    return base_content
