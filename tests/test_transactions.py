from typing import Dict, Any

import pytest
import requests

from .types import spy
from proof_business_api import ProofClient

pytestmark = [pytest.mark.vcr]

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


@pytest.fixture
def client(api_key: str) -> ProofClient:
    return ProofClient(api_key, fairfax=True)


def test_list(client: ProofClient, spies: spy):
    response = client.transactions.all()

    getspy = spies["get"]
    getspy.assert_called_once()

    assert all([key in response for key in ["total_count", "count", "data"]])


def test_lifecycle(client: ProofClient, spies: spy):
    # Create a new transaction
    response = client.transactions.create(**_create_params)
    post_spy = spies["post"]
    post_spy.assert_called_once()

    # Fetch it back to confirm it was received
    response = client.transactions.retrieve(response["id"])
    get_spy = spies["get"]
    get_spy.assert_called_once()
    get_spy.reset_mock()

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
            get_spy.reset_mock()
    else:
        raise AssertionError("Unable to fetch document")

    # Delete the transaction to clean up after ourselves
    response = client.transactions.delete(transaction_id)
    deletespy = spies["delete"]
    deletespy.assert_called_once()
