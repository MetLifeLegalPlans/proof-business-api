import logging
import os

import pytest
import requests


@pytest.fixture
def api_key() -> str:
    return os.environ.get("PROOF_API_KEY", default=None)


@pytest.hookimpl(tryfirst=True)
def pytest_exception_interact(
    node: pytest.Item, call: pytest.CallInfo, report: pytest.TestReport
):
    if call.excinfo.type is requests.HTTPError:
        print(call.excinfo.value.response.json())
