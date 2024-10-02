import logging
import os
from typing import Optional

import pytest
import requests


@pytest.fixture
def api_key() -> Optional[str]:
    return os.environ.get("PROOF_API_KEY", default=None)


@pytest.hookimpl(tryfirst=True)
def pytest_exception_interact(
    node: pytest.Item,
    call: pytest.CallInfo,
    report: pytest.TestReport,
):
    if call.excinfo and call.excinfo.type is requests.HTTPError:
        # pyre-ignore[16]
        print(call.excinfo.value.response.json())
