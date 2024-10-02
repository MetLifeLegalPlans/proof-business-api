import pytest
from faker import Faker
from proof_business_api.client import Client
from proof_business_api.transactions import TransactionsClient
from proof_business_api.resource import ProofClient

import requests

fake = Faker()


@pytest.fixture
def api_key() -> str:
    return "".join(fake.random_letters(length=8))


def test_client_uses_correct_url(api_key) -> None:
    client = Client(api_key, fairfax=True)
    assert "fairfax" in client.base_url

    client = Client(api_key, fairfax=False)
    assert "fairfax" not in client.base_url


def test_client_puts_key_in_headers(api_key) -> None:
    client = Client(api_key)
    assert "ApiKey" in client.headers and client.headers["ApiKey"] == api_key


def test_client_provides_document_url_version(api_key) -> None:
    versions = ["v1", "v2"]
    for version in versions:
        client = Client(api_key, document_url_version=version)
        assert client.url_version_params["document_url_version"] == version

    with pytest.raises(AssertionError):
        Client(api_key, document_url_version="v3")


def test_client_joins_resources_properly(api_key, mocker) -> None:
    class MyClient(Client):
        resource = api_key

    client = MyClient(api_key)
    assert f"v1/{api_key}" in client.base_url

    client = TransactionsClient(api_key)
    mocker.patch("requests.get")

    client.all()
    requests.get.assert_called_once_with(client.base_url, headers=client.headers, params={})


def test_resource_client_initializes_subresources(api_key) -> None:
    client = ProofClient(api_key)
    assert client.transactions.api_key == api_key
