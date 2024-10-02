from typing import Dict, Any

import pytest
from pytest_mock import MockerFixture, MockType

import requests

from proof_business_api import ProofClient

_api_key_var = "PROOF_API_KEY"
pytestmark = [pytest.mark.vcr]

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
def client(api_key: str) -> ProofClient:
    return ProofClient(api_key, fairfax=True)


def _reset_spies() -> None:
    for spy in _spies.values():
        spy.reset_mock()


def test_list(client: ProofClient):
    response = client.transactions.all()

    get_spy = _spies["get"]
    get_spy.assert_called_once()

    assert all([key in response for key in ["total_count", "count", "data"]])


def test_lifecycle(client: ProofClient):
    # Create a new transaction
    response = client.transactions.create(**_create_params)
    post_spy = _spies["post"]
    post_spy.assert_called_once()

    # Fetch it back to confirm it was received
    response = client.transactions.retrieve(response["id"])
    get_spy = _spies["get"]
    get_spy.assert_called_once()
    _reset_spies()

    transaction_id = response["id"]
    document_id = response["documents"][0]["id"]

    # Fetch its document object - this can take some time to finish processing
    for _ in range(3):
        try:
            response = client.transactions.get_document_from(
                transaction_id,
                document_id,
            )
            get_spy.assert_called_once()
            break
        except requests.HTTPError:
            _reset_spies()
    else:
        raise AssertionError("Unable to fetch document")

    # Delete the transaction to clean up after ourselves
    response = client.transactions.delete(transaction_id)
    delete_spy = _spies["delete"]
    delete_spy.assert_called_once()
