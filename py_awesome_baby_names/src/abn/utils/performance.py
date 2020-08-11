"""The performance modules includes tools to manage algorthm performance.
"""

import time
from typing import Callable


class Timer:
    """Timer class provides tools to time code performance.
    """
    def __init__(self) -> None:
        __start = 0
        __end = 0

    def start(self) -> None:
        """Start the timer.
        """
        self.__start = time.time()

    def end(self, m: str = "") -> None:
        """End the timer.

        Args:
            m (str): Message to be prefixed to the time.
        """
        self.__end = time.time()
        print("{:s}{:f}".format(m, self.__end - self.__start))


def time_it(func: Callable) -> Callable:
    """Decorator function to time the performance of the function. Result in
    seconds will be printed.

    Returns:
        Callable: A new function with timer added.
    """
    def new_function(*args: list, **kwargs: dict) -> object:
        t = Timer()
        t.start()
        result = func(*args, **kwargs)
        t.end("Time:")
        return result
    return new_function
