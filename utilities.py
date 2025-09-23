#!/usr/bin/python

from inspect import getframeinfo, currentframe
from typing import Optional, Any, Dict, List, Union
from os import stat, system
from re import sub


def _line():
    info = getframeinfo(currentframe().f_back)[0:3]
    return info[1]


def is_not_empty_value(val: Any) -> bool:
    return val is not None and (val != "" or len(val) > 0)


def sprintf(target: str, *replacements: Union[str, int, float]):
    for x, r in enumerate(replacements):
        target = sub(f"{{%{x}%}}", str(r), target)
    return target


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


def printerr(message: str):
    print(f"❌ {message}")


def printinf(message: str):
    print(f"ℹ️ {message}")


def printalr(message: str):
    print(f"⚠️ {message}")


def printsuc(message: str):
    print(f"✅ {message}")


def try_install(module_name: str):
    global modules

    command = modules[module_name]["command"]

    print(f"Executing {command}...\n")
    try:
        system(command)
    except Exception as e:
        printerr(e)
        exit()

    print("Restart the console to see the changes")
    exit()


def display_error_message(module_name: str):
    global modules

    url = modules[module_name]["url"]

    printalr(f"Package {module_name} is required\n")

    response = input("Would you like to install it now? (yes/no) ")
    if "yes" == response:
        try_install(module_name)
    else:
        print("See {url} for more details\n")
    exit()

