from contextlib import contextmanager
from typing import Generator

import pytest

@contextmanager
def assert_not_raise(exception: type[BaseException]) -> Generator[None, None, None]:
    try:
        yield
    except exception:
        pytest.fail(f"DID RAISE {exception}")
