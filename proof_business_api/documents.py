from .client import Client
from .types import JsonObj


class DocumentsClient(Client):
    resource = "documents"

    def update(self, id: str, **payload) -> JsonObj:
        return self._put(id, json=payload, params=self.url_version_params)

    def delete(self, id: str) -> JsonObj:
        return self._delete(id)

    # Adding and retrieving documents is handled in the transactions controller
