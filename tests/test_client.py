import pytest
from faker import Faker
from proof_business_api.client import Client

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
