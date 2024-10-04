import inspect

from .client import Client

from .transactions import TransactionsClient
from .documents import DocumentsClient
from .webhooks import WebhooksClient


class ProofClient:
    transactions = TransactionsClient("")
    documents = DocumentsClient("")
    webhooks = WebhooksClient("")

    def __init__(self, *args, **kwargs) -> None:
        for name, member in inspect.getmembers(self):
            cls = type(member)
            if issubclass(cls, Client):
                setattr(self, name, cls(*args, **kwargs))
