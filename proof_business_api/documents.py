from .client import Client
from .types import JsonObj

from urllib.parse import urljoin


class DocumentsClient(Client):
    resource = "documents"
