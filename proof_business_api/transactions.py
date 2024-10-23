from .client import Client
from .types import JsonObj

from urllib.parse import urljoin


class TransactionsClient(Client):
    resource = "transactions"

    def all(self, **params) -> JsonObj:
        """
        Lists the currently active translations in chronological order by creation time.

        :param params:

        :key limit: (``integer``) -- Optional. How many results to return. Max 1000. (Default 10)
        :key offset: (``integer``) -- Optional. Offset request by a given number of items. (Default 0)
        :key created_date_start: (``ISO-8061 DateTime String``) -- Optional. Will return all transactions updated after specified time. May contain timezone offset.
        :key created_date_end:  (``ISO-8061 Datetime String``) -- Optional. Will return all transactions updated before specified time. May contain timezone offset.
        :key transaction_status:  (``string``) -- Return transactions based on current status. (started, sent, received, completed, partially_completed, completed_with_rejections, active, sent_to_closing_ops, sent_to_title_agency, expired)
        :key document_url_version:  (``string``) -- Control documents and signer photo identifications download URLs. (v1 - AWS S3 pre-signed URLs, v2 - Proof secure URLs)


        :return: ``JsonObj``

        `Proof Docs <https://dev.proof.com/reference/getalltransactions>`_

        """
        return self._get("", params=params)

    def create(self, document_url_version: str = "v1", **payload) -> JsonObj:
        """
        Created a document transaction. Additional arguments documented in Proof docs.

        * ``signer`` object

            * email (``string``) -- Required. Recipient's email. Can use recipient_group instead.
            * first_name (``string``) -- First Name
            * last_name (``string``) -- Last Name

        * ``signers`` (``object[]``)

            * An array of ``signer`` objects with an order key for determining signing order
            * order (``integer``) -- Order the signers will sign in. Setting to the same order as another signer indicates they sign at the same time.
            * email (``string``) -- Email of signer. Email is required unless you have a recipient_group object.


        :param document_url_version: (``string``) -- Document URL version, see proof docs. Default "v1"
        :param payload:

        :key signer: (``signer Object``)
        :key signers: (``signers Object``)
        :key activation_time: (``ISO-8061 Datetime String``) -- Optional. Sets the time after which signer is permitted to connect to a notary. Timezone defaults to account timezone if not provided.
        :key transaction_type: (``string``) Short, human-readable description of transaction.
        :key document: (``string``) Documents to be signed or notarized. Accepted as an array of document objects or simple document["resource"] field values.

        :return: ``JsonObj``

        `Proof Docs <https://dev.proof.com/reference/createtransaction>`_
        """
        return self._post(
            "",
            params=self.url_version_params,
            json=payload,
        )

    def retrieve(self, id: str, **params) -> JsonObj:
        """
        Retrieves document with given ID.
        :param id: (``string``) -- Transaction ID.
        :param params:

        :return: (``JsonObj``) -- Returns a transaction object if successful.

        `Proof Docs <https://dev.proof.com/reference/gettransaction>`_
        """
        return self._get(id, params=params)

    def update_draft(self, id: str, **payload) -> JsonObj:
        """
        Updates "draft" transactions.

        :param id: (``string``) -- ID of transaction to update.
        :param payload: Params are largely the same as `create`. Refer to documentation for details.

        :key signer: (``signer Object``)
        :key signers: (``signers Object``)
        :key activation_time: (``ISO-8061 Datetime String``) -- Optional. Sets the time after which signer is permitted to connect to a notary. Timezone defaults to account timezone if not provided.
        :key transaction_type: (``string``) Short, human-readable description of transaction.
        :key documents: (``Object[]``) Array of objects containing `document_id` ``string`` and bundle_position ``integer``.

        :return: ``JsonObj``

        `Proof Docs <https://dev.proof.com/reference/updatedrafttransaction>`_
        """
        return self._put(
            id,
            params=self.url_version_params,
            json=payload,
        )

    def delete(self, id: str) -> JsonObj:
        """
        Deleted the transaction with a specified ID.

        :param id: (``string``) -- The ID of the transaction to delete.

        :return: ``JsonObj``

        `Proof Docs <https://dev.proof.com/reference/deletetransaction>`_
        """
        return self._delete(id)

    def activate_draft(self, id: str, **payload) -> JsonObj:
        """
        Activates a draft transaction. This will initiate the document notarization workflow if the transaction was started as a draft.

        :param id: (``string``) -- Transaction ID to activate.
        :param payload:

        :key document_url_version: (``string``) -- Document URL version, see proof docs. Default "v1"

        :return: ``JsonObj``

        `Proof Docs <https://dev.proof.com/reference/activatedrafttransaction>`_
        """
        return self._post(
            urljoin(f"{id}/", "notarization_ready"),
            params=self.url_version_params,
            json=payload,
        )

    def resend_email(self, id: str, **params) -> JsonObj:
        """
        Resends transaction email to signer for a given transaction ID.

        :param id: (``string``) -- Transaction ID for which to send the email.
        :param params:

        :key message_to_signer: (``string``) -- Message to signer using GitHub Flavored Markdown. HTML, images, links and code are stripped.
        :key document_url_version: (``string``) -- Document URL version, see proof docs. Default "v1"

        :return: ``JsonObj``

        `Proof Docs <https://dev.proof.com/reference/resendtransactionemail>`_
        """
        return self._post(urljoin(f"{id}/", "send_email"), params=params)

    def resend_sms(self, id: str, **params) -> JsonObj:
        """
        Resends transaction SMS for a given transaction ID. The phone number values associated with the transaction signers will be used.


        :param id: (``string``) -- Transaction ID for which to send the SMS.
        :param params:

        :return: ``JsonObj``

        `Proof Docs <https://dev.proof.com/reference/resendtransactionsms>`_
        """
        return self._post(urljoin(f"{id}/", "send_sms"), params=params)

    def eligible_notaries_for(self, id: str) -> JsonObj:
        """
        Returns eligible notaries for given transaction ID.

        :param id: (``string``) -- Transaction ID for which to retrieve the notaries.
        :return:

        `Proof Docs <https://dev.proof.com/reference/getalleligiblenotaries>`_
        """
        return self._get(urljoin(f"{id}/", "notaries"))

    def add_document_to(self, id: str, **payload) -> JsonObj:
        """
        Adds documents to draft transaction.

        :param id: (``string``) -- Transaction ID for which to add a document.
        :param payload:

        :key filename: (``string``) -- Plain language document name.
        :key resource: (``string``) -- Document file resource. Accepted values can be a URL pointing to the PDF file, the full contents of the PDF file in Base64 encoding, the file itself as a direct upload, or a template permalink string pointing to a preconfigured PDF. The maximum accepted file size is 30MB.
        :key requirement: (``string``) -- See docs for details.
        :key bundle_position: (``integer``) -- Position in document bundle.
        :key esign_required: (``boolean``)
        :key identity_confirmation_required: (``boolean``)

        :return:

        `Proof Docs <https://dev.proof.com/reference/adddocument>`_
        """
        return self._post(
            urljoin(f"{id}/", "documents"),
            params=self.url_version_params,
            json=payload,
        )

    def get_document_from(self, id: str, document_id: str, **params) -> JsonObj:
        """
        Returns a base64 encoded version of a document object attached to a transaction.
        Document state will be reflected by the status of the transaction.

        :param id: (``string``) -- ID of transaction from which to get the document.
        :param document_id: (``string``) -- ID of the document to retrieve.
        :param params:

        :return:

        `Proof Docs <https://dev.proof.com/reference/getdocument>`_
        """
        return self._get(f"{id}/documents/{document_id}", params=params)
