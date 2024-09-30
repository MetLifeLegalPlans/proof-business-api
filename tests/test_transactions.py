from typing import Dict, Any
import os

import pytest
from pytest_mock import MockerFixture, MockType

import requests

from proof_business_api.transactions import TransactionsClient

_api_key_var = "PROOF_API_KEY"
pytestmark = pytest.mark.skipif(
    not os.environ.get(_api_key_var, default=None), reason="No test API key provided"
)

_used_methods = ["get", "post", "put", "patch", "delete"]
_spies: Dict[str, MockType] = {}
_create_params: Dict[str, Any] = {
    "signer": {
        "email": "test@willing.com",
        "first_name": "CI",
        "last_name": "Test",
    },
    "document": "JVBERi0xLjcKCjEgMCBvYmogICUgZW50cnkgcG9pbnQKPDwKICAvVHlwZSAvQ2F0YWxvZwogIC9QYWdlcyAyIDAgUgo+Pgplbm\
RvYmoKCjIgMCBvYmoKPDwKICAvVHlwZSAvUGFnZXMKICAvTWVkaWFCb3ggWyAwIDAgMjAwIDIwMCBdCiAgL0NvdW50IDEKICAvS2lkcyBbID\
MgMCBSIF0KPj4KZW5kb2JqCgozIDAgb2JqCjw8CiAgL1R5cGUgL1BhZ2UKICAvUGFyZW50IDIgMCBSCiAgL1Jlc291cmNlcyA8PAogICAgL\
0ZvbnQgPDwKICAgICAgL0YxIDQgMCBSIAogICAgPj4KICA+PgogIC9Db250ZW50cyA1IDAgUgo+PgplbmRvYmoKCjQgMCBvYmoKPDwKICAvV\
HlwZSAvRm9udAogIC9TdWJ0eXBlIC9UeXBlMQogIC9CYXNlRm9udCAvVGltZXMtUm9tYW4KPj4KZW5kb2JqCgo1IDAgb2JqICAlIHBhZ2UgY29\
udGVudAo8PAogIC9MZW5ndGggNDQKPj4Kc3RyZWFtCkJUCjcwIDUwIFRECi9GMSAxMiBUZgooSGVsbG8sIHdvcmxkISkgVGoKRVQKZW5kc3RyZ\
WFtCmVuZG9iagoKeHJlZgowIDYKMDAwMDAwMDAwMCA2NTUzNSBmIAowMDAwMDAwMDEwIDAwMDAwIG4gCjAwMDAwMDAwNzkgMDAwMDAgbiAK\
MDAwMDAwMDE3MyAwMDAwMCBuIAowMDAwMDAwMzAxIDAwMDAwIG4gCjAwMDAwMDAzODAgMDAwMDAgbiAKdHJhaWxlcgo8PAogIC9TaXplIDYK\
ICAvUm9vdCAxIDAgUgo+PgpzdGFydHhyZWYKNDkyCiUlRU9G",
}


@pytest.fixture(autouse=True)
def lifecycle(mocker: MockerFixture):
    for method in _used_methods:
        _spies[method] = mocker.spy(requests, method)

    yield


@pytest.fixture
def client(api_key: str) -> str:
    return TransactionsClient(api_key, fairfax=True)


def test_list(client: TransactionsClient):
    response = client.all()

    get_spy = _spies["get"]
    get_spy.assert_called_once()

    assert all([key in response for key in ["total_count", "count", "data"]])


def test_lifecycle(client: TransactionsClient):
    response = client.create(**_create_params)
    post_spy = _spies["post"]
    post_spy.assert_called_once()

    response = client.retrieve(response["id"])
    get_spy = _spies["get"]
    get_spy.assert_called_once()

    response = client.delete(response["id"])
    delete_spy = _spies["delete"]
    delete_spy.assert_called_once()
