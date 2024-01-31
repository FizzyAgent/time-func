import concurrent.futures as futures
from functools import wraps
from typing import Callable

from _utils.newtypes import Param, RetType


def timeout(
    max_wait: float,
    on_timeout: Exception = TimeoutError(),
    *,
    executor: futures.Executor = futures.ThreadPoolExecutor(),
) -> Callable[[Callable[Param, RetType]], Callable[Param, RetType]]:
    """
    Timeout a function after a certain amount of time
    Does not actually terminate the function on timeout, but will unblock the thread
    """

    def decorator(func: Callable[Param, RetType]) -> Callable[Param, RetType]:
        @wraps(func)
        def wrapper(*args: Param.args, **kwargs: Param.kwargs) -> RetType:
            future = executor.submit(lambda: func(*args, **kwargs))
            try:
                return future.result(timeout=max_wait)
            except futures.TimeoutError:
                raise on_timeout

        return wrapper

    return decorator
