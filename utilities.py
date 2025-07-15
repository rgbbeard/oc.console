from inspect import getframeinfo, currentframe
from typing import Optional, Any, Dict, List, Union


def _line():
    info = getframeinfo(currentframe().f_back)[0:3]
    return info[1]


def is_not_empty_value(val: Any) -> bool:
    return val is not None and (val != "" or len(val) > 0)


def array_clear(
    target: Optional[Union[dict, list]], 
    check_values: bool = True,
    maintain_index: bool = False
) -> Union[Dict[Any, Any], List[Any]]:
    result = {} if maintain_index else []

    if target is not None:
        if isinstance(target, dict):
            iterator = target.items()
        elif isinstance(target, list):
            iterator = enumerate(target)
        else:
            raise TypeError("Input must be a dict or list")

        for index, value in iterator:
            if (check_values and is_not_empty_value(value)) or (not check_values and index):
                item = value if check_values else index
                if maintain_index:
                    result[index] = item
                else:
                    result.append(item)

    return result
