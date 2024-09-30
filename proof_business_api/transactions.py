from .client import Client
from .types import JsonObj

from urllib.parse import urljoin


class TransactionsClient(Client):
    resource = "transactions"

    def all(self, **params) -> JsonObj:
        return self._get("", params=params)

    def create(self, document_url_version: str = "v1", **payload) -> JsonObj:
        return self._post(
            "",
            params=self.url_version_params,
            json=payload,
        )

    def retrieve(self, id: str, **params) -> JsonObj:
        return self._get(id, params=params)

    def update_draft(self, id: str, **payload) -> JsonObj:
        return self._put(
            id,
            params=self.url_version_params,
            json=payload,
        )

    def delete(self, id: str) -> JsonObj:
        return self._delete(id)

    def activate_draft(self, id: str, **payload) -> JsonObj:
        return self._post(
            urljoin(f"{id}/", "notarization_ready"),
            params=self.url_version_params,
            json=payload,
        )

    def resend_email(self, id: str, **params) -> JsonObj:
        return self._post(urljoin(f"{id}/", "send_email"), params=params)

    def resend_sms(self, id: str, **params) -> JsonObj:
        return self._post(urljoin(f"{id}/", "send_sms"), params=params)

    def eligible_notaries_for(self, id: str) -> JsonObj:
        return self._get(urljoin(f"{id}/", "notaries"))

    def add_document_to(
        self,
        id: str,
        **payload,
    ) -> JsonObj:
        return self._post(
            urljoin(f"{id}/", "documents"),
            params=self.url_version_params,
            json=payload,
        )

    def get_document_from(self, id: str, document_id: str, **params) -> JsonObj:
        return self._get(f"{id}/documents/{document_id}", params=params)
