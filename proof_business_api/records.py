from .client import Client
from .types import JsonObj
import requests


class NotarizationRecordsClient(Client):
    resource = "notarization_records"

    def all(self, **params) -> JsonObj:
        """
        Lists all notarization records in chronological order by creation time.

        :param params:

        :key limit: (``integer``) -- Optional. How many results to return. (Default 20)
        :key offset: (``integer``) -- Optional. Offset request by a given number of items. (Default 0)

        :return: ``JsonObj``

        `Proof Docs <https://dev.proof.com/reference/getnotarizationrecords>`_
        """
        return self._get("", params=params)

    def retrieve(self, id: str, **params) -> JsonObj:
        """
        Retrieves the specified notarization record with given ID.

        :param id: (``string``) -- ID of the notarization record to retrieve
        :param params:

        :return: ``JsonObj``

        `Proof Docs <https://dev.proof.com/reference/getnotarizationrecord>`_
        """
        return self._get(id, params=params)

    def retrieve_from_url(self, url: str, **params) -> JsonObj:
        return self.retrieve(url.split("/")[-1], **params)

    def fetch_video(self, url: str) -> bytes:
        # They require our API key be sent to a non-resource route
        # to authenticate the download, so use bare requests
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.content
