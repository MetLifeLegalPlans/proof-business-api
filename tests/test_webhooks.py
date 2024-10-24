from faker import Faker
import pytest, os, hmac

from .types import spy
from proof_business_api import ProofClient
from hashlib import sha256

pytestmark = [pytest.mark.vcr]
fake = Faker()
url = "https://test.example.com"


@pytest.fixture
def client(api_key: str) -> ProofClient:
    return ProofClient(api_key, fairfax=True)


@pytest.fixture
def custom_header() -> str:
    return "X-Security-Key:{}".format("".join(fake.random_letters(length=8)))


@pytest.fixture
def proof_api_key() -> str:
    return os.environ.get("PROOF_API_KEY")


def test_validation(client: ProofClient, proof_api_key: str):
    api_key = proof_api_key
    body_text = fake.text()
    body = body_text.encode()
    generated_hmac = hmac.new(api_key.encode(), body, sha256).hexdigest()
    valid = client.webhooks.validate_hmac(body, generated_hmac)
    assert valid == True



def test_list(client: ProofClient, spies: spy):
    response = client.webhooks.all()

    get_spy = spies["get"]
    get_spy.assert_called_once()

    assert response is not None

def test_subscriptions(client: ProofClient, spies: spy):
    response = client.webhooks.subscriptions()

    get_spy = spies["get"]
    get_spy.assert_called_once()

    assert response["transaction"]


def test_lifecycle(client: ProofClient, spies: spy, custom_header: str):
    webhook = client.webhooks.create(
        url=url,
        subscriptions=["transaction.completed"],
        header=custom_header,
    )

    # Not checking the actual URLs returned as
    assert "url" in webhook.keys()
    assert "X-Security-Key" in webhook["header"]

    new_url = fake.url(schemes=["https"])
    response = client.webhooks.update(webhook["id"], url=new_url)
    assert response["updated"]

    webhook = client.webhooks.retrieve(webhook["id"])
    assert "X-Security-Key" in webhook["header"]

    response = client.webhooks.delete(webhook["id"])
    assert response["deleted"]
