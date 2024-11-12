import inspect

from .client import Client

from .transactions import TransactionsClient
from .documents import DocumentsClient
from .webhooks import WebhooksClient
from .records import NotarizationRecordsClient


class ProofClient:
    transactions = TransactionsClient("")
    documents = DocumentsClient("")
    webhooks = WebhooksClient("")
    records = NotarizationRecordsClient("")

    def __init__(self, *args, **kwargs) -> None:
        for name, member in inspect.getmembers(self):
            cls = type(member)
            if issubclass(cls, Client):
                setattr(self, name, cls(*args, **kwargs))
