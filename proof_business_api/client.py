import requests
from typing import Dict, Any

from urllib.parse import urljoin


class Client:
    """
    A basic client for Proof.com's Business API.
    """

    fairfax: bool = False
    resource: str = ""

    def __init__(self, api_key: str, fairfax: bool = False) -> None:
        self.api_key = api_key
        self.fairfax = fairfax

    @property
    def headers(self) -> Dict[str, str]:
        return {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "ApiKey": self.api_key,
        }

    @property
    def base_url(self) -> str:
        return urljoin(
            "https://api.{}proof.com/v1".format("fairfax." if self.fairfax else ""),
            self.resource,
        )

    def request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        url = urljoin(self.base_url, endpoint)
        res = getattr(requests, method)(url, headers=self.headers, **kwargs)
        res.raise_for_status()
        return res.json()

    def get(self, endpoint: str, **kwargs) -> Dict:
        return self.request("get", endpoint, **kwargs)

    def post(self, endpoint: str, **kwargs) -> Dict:
        return self.request("post", endpoint, **kwargs)

    def put(self, endpoint: str, **kwargs) -> Dict:
        return self.request("put", endpoint, **kwargs)

    def patch(self, endpoint: str, **kwargs) -> Dict:
        return self.request("patch", endpoint, **kwargs)

    def delete(self, endpoint: str, **kwargs) -> Dict:
        return self.request("delete", endpoint, **kwargs)
