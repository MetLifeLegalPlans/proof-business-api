import requests
from typing import Dict, Any

from urllib.parse import urljoin

_valid_versions = ["v1", "v2"]


class Client:
    """
    A basic client for Proof.com's Business API.
    """

    fairfax: bool = False
    document_url_version: str = "v1"
    api_version: str = "v1"
    resource: str = ""

    def __init__(
        self,
        api_key: str,
        fairfax: bool = False,
        document_url_version: str = "v1",
    ) -> None:
        self.api_key = api_key
        self.fairfax = fairfax
        self.document_url_version = document_url_version

        assert document_url_version in _valid_versions
        assert self.api_version in _valid_versions

    @property
    def headers(self) -> Dict[str, str]:
        return {
            "Content-Type": "application/json",
            "ApiKey": self.api_key,
        }

    @property
    def base_url(self) -> str:
        return urljoin(
            "https://api.{}proof.com/{}/".format(
                ("fairfax." if self.fairfax else ""),
                self.api_version,
            ),
            self.resource + "/",
        )

    @property
    def url_version_params(self) -> Dict[str, str]:
        return {"document_url_version": self.document_url_version}

    def request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        url = urljoin(f"{self.base_url}", endpoint)
        res = getattr(requests, method)(url, headers=self.headers, **kwargs)
        res.raise_for_status()
        return res.json()

    def _get(self, endpoint: str, **kwargs) -> Dict:
        return self.request("get", endpoint, **kwargs)

    def _post(self, endpoint: str, **kwargs) -> Dict:
        return self.request("post", endpoint, **kwargs)

    def _put(self, endpoint: str, **kwargs) -> Dict:
        return self.request("put", endpoint, **kwargs)

    def _patch(self, endpoint: str, **kwargs) -> Dict:
        return self.request("patch", endpoint, **kwargs)

    def _delete(self, endpoint: str, **kwargs) -> Dict:
        return self.request("delete", endpoint, **kwargs)
