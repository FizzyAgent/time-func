import time
from typing import Callable

import pytest

from time_utils import timeout


def get_timeout_sleep(x: float) -> Callable[[float], float]:
    @timeout(x)
    def timeout_sleep(y: float) -> float:
        time.sleep(y)
        return y

    return timeout_sleep


def test_timeout_decorator() -> None:
    for timeout_limit in range(1, 5):
        timeout_sleep = get_timeout_sleep(timeout_limit)
        for base_sleep in range(5):
            sleep_for = base_sleep + 0.1
            if sleep_for > timeout_limit:
                with pytest.raises(TimeoutError):
                    timeout_sleep(sleep_for)
            else:
                try:
                    assert timeout_sleep(sleep_for) == sleep_for
                except TimeoutError:
                    pytest.fail(
                        f"Function timed out after {timeout_limit}s despite sleeping for {sleep_for}s"
                    )
