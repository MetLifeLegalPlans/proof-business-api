import os
from typing import Optional, Dict, Any

import pytest
from pytest_mock import MockerFixture, MockType
import requests


_used_methods = ["get", "post", "put", "patch", "delete"]
_spies: Dict[str, MockType] = {}


def _resetspies() -> None:
    for spy in _spies.values():
        spy.reset_mock()


@pytest.fixture(autouse=True)
def lifecycle(mocker: MockerFixture):
    for method in _used_methods:
        _spies[method] = mocker.spy(requests, method)

    yield

    _resetspies()


@pytest.fixture(scope="module")
def vcr_config() -> Dict[str, Any]:
    return {"filter_headers": ["ApiKey"]}


@pytest.fixture
def spies() -> Dict[str, MockType]:
    return _spies


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
