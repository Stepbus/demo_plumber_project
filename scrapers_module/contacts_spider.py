import requests

from dao_module.dao_models import Client
from logger_module.logger_ import logger, user_log_name
from scrapers_module.services import headers, query_myproposalslist, variables_myproposalslist, proxies, query_chat


class ContactsSpider:
    url = "https://api/graphql"

    def __init__(self):
        self.contacts_id_dict: list[dict] = []

    def _make_web_request_all(self) -> dict:
        logger.log(user_log_name, f"Request for receiving all clients from page with contacts")
        try:
            response = requests.request("POST", self.url, headers=headers,
                                        json={"query": query_myproposalslist, "variables": variables_myproposalslist},
                                        proxies=proxies[0], timeout=15)
            response.raise_for_status()
        except requests.exceptions.RequestException:
            raise
        work_requests_dict = response.json()
        return work_requests_dict

    def _make_request_one(self, id_) -> dict:
        try:
            response = requests.request("POST", self.url, headers=headers,
                                        json={"query": query_chat, "variables": {"id": id_}}, proxies=proxies[0],
                                        timeout=10)
            response.raise_for_status()
        except requests.exceptions.RequestException:
            raise
        work_requests_dict = response.json()
        return work_requests_dict

    def _get_inner_client_id(self, request: dict):
        result = request["data"]["serviceRequestList"]['edges']
        for client in result:
            client_id = client['node']['id']
            client_id_contact = client['node']['proposal']['id']
            self.contacts_id_dict.append({"client_id": client_id, "client_id_contact": client_id_contact})

    def get_additional_info(self) -> list[Client]:
        clients_with_filled_contact: list[Client] = []
        if self.contacts_id_dict:
            for client in self.contacts_id_dict:
                additional_info = self._make_request_one(client.get("client_id_contact"))
                client: Client = client.get("client")
                client_contacts: dict = additional_info["data"]['serviceRequestByProposalId']["consumer"]
                client.contact_name = client_contacts.get('name')
                client.contact_phone = client_contacts.get('phone')
                client.contact_email = client_contacts.get('email')
                clients_with_filled_contact.append(client)
        return clients_with_filled_contact

    def run(self):
        res = self._make_web_request_all()
        self._get_inner_client_id(res)
