from .client import Client
from .types import JsonObj


class WebhooksClient(Client):
    resource = "webhooks"
    api_version = "v2"

    def all(self, **params) -> JsonObj:
        """
        Lists all active webhooks.

        :param params:
        :return: ``JsonObj``

        `Proof Docs <https://dev.proof.com/reference/getallmortgagewebhooksv2>`_
        """
        return self._get("", params=params)

    def create(self, **payload) -> JsonObj:
        """
        Creates a webhook which will call the provided URL with provided headers for given subscriptions.

        :param payload:

        :key url: (``string``) -- The URL to send to for each subscribed event.
        :key header: (``string | null``) -- Header value to pass through to requests. Ex: `"ApiKey": "<API_KEY>"`
        :key subscriptions: (``string[]``) -- Array containing events for which to POST a webhook. See `Docs <https://dev.proof.com/docs/webhooks-v2>`_ for valid subscriptions.

        :return: ``JsonObj``

        `Proof Docs <https://dev.proof.com/reference/createmortgagewebhookv2>`_
        """
        return self._post("", json=payload)

    def retrieve(self, id: str, **params) -> JsonObj:
        """
        Retrieves the specified webhook with given ID.

        :param id: (``string``) -- ID of webhook to retrieve.
        :param params:

        :return: ``JsonObj``

        `Proof Docs <https://dev.proof.com/reference/getmortgagewebhookurl>`_
        """
        return self._get(id, params=params)

    def update(self, id: str, **payload) -> JsonObj:
        """
        Updates the webhook with the given ID.

        :param id: (``string``) -- ID of webhook to update.
        :param payload:

        :key url: (``string``) -- URL to use for subscription events.
        :key header: (``string | null``) -- Header to pass through for each request.
        :key subscriptions: (``string[]``) -- Array containing events for which to POST a webhook. See `Docs <https://dev.proof.com/docs/webhooks-v2>`_ for valid subscriptions.


        :return: ``JsonObj``

        `Proof Docs <https://dev.proof.com/reference/updatemortgagewebhookv2>`_
        """
        return self._put(id, json=payload)

    def delete(self, id: str) -> JsonObj:
        """
        Deletes the webhook for the given ID.

        :param id: (``string``) -- ID of the webhook to be deleted.

        :return: ``JsonObj``

        `Proof Docs <https://dev.proof.com/reference/deletemortgagewebhookv2>`_
        """
        return self._delete(id)

    def events_for(self, id: str, **params) -> JsonObj:
        """
        Lists events for the webhook with given ID.

        :param id: (``string``) -- ID of the webhook for witch to get events.
        :param params:

        :return: ``JsonObj``


        `Proof Docs <https://dev.proof.com/reference/getmortgagewebhookeventsv2>`_
        """
        return self._get(id, params=params)

    def subscriptions(self) -> JsonObj:
        """
        Returns all possible subscription events.

        :return: ``JsonObj``
        """
        return self._get("subscriptions")
