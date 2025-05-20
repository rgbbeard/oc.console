import inspect


def _line():
    info = inspect.getframeinfo(inspect.currentframe().f_back)[0:3]
    return info[1]
