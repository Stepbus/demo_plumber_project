import requests

from dao_module.dao import Dao
from dao_module.dao_models import Client, KeyWords, IgnoreWords
from email_notification_module.email_notification import send_email
from logger_module.logger_ import user_log_name, logger
from scrapers_module.contacts_spider import ContactsSpider
from scrapers_module.exceptions import PageDoesNotOpen, NoSuchElementError
from scrapers_module.interest_spider import InterestSpider
from scrapers_module.new_job_spider import NewJobSpider


class TaskManager:
    dao = Dao()
    patter_url_proposition = 'https://www./service-pro//{}'

    @property
    def last_work_request(self):
        last_work_request = self.dao.get_last_record(Client)
        if last_work_request:
            return last_work_request.client_id

    @property
    def key_words(self):
        return self.dao.get_all(KeyWords)

    @property
    def ignore_words(self):
        return self.dao.get_all(IgnoreWords)

    def get_new_work_requests(self):
        new_job_spider = NewJobSpider(self.last_work_request, self.key_words, self.ignore_words)
        try:
            new_requests = new_job_spider.run()
        except requests.exceptions.RequestException:
            raise
        except Exception:
            raise
        clients = [Client(**client) for client in new_requests]
        return clients

    def save_new_work_requests(self, clients):
        saved_new_clients = []
        if all([isinstance(client, Client) for client in clients]):
            saved_new_clients: list = self.dao.create_all(clients)
        return saved_new_clients

    def make_url(self, clients: list):
        url_proposition = []
        for client in clients:
            url_ = self.patter_url_proposition.format(client.client_id)
            url_proposition.append(url_)
            client.client_url = url_
            self.dao.update(client)
        logger.log(user_log_name, f"{url_proposition=}")
        logger.log(user_log_name, f"{clients=}")
        return url_proposition

    def apply_job_request(self, url_proposition):
        interest_spider = InterestSpider()
        try:
            result = interest_spider.run(url_proposition)
        except Exception:
            raise
        finally:
            if interest_spider.browser:
                interest_spider.browser.quit_browser()
        return result

    def update_client_info(self, additional_info_list):
        for client_info in additional_info_list:
            client_list = self.dao.get_by_field(Client, {'client_id': client_info.get('client_id')})
            if client_list:
                client = client_list[0]
                client.type_klus = client_info.get('type_klus')[:400] if client_info.get('type_klus') else None
                client.soort_probleem = client_info.get('soort_probleem')[:400] if client_info.get('soort_probleem') else None
                client.aanvullende_informatie = client_info.get('aanvullende_informatie')[:700] if client_info.get(
                    'aanvullende_informatie') else None
                self.dao.update(client)

    def get_contact_info(self):
        prepared_for_get_contact_info: list[dict] = []
        contact_spider = ContactsSpider()
        contact_spider.run()
        for contact in contact_spider.contacts_id_dict:
            client_list: list[Client] = self.dao.get_by_field(Client, {'client_id': contact.get('client_id')})
            if client_list:
                client: Client = client_list[0]
                if not any([client.contact_name, client.contact_phone, client.contact_email]):
                    contact.update({"client": client})
                    prepared_for_get_contact_info.append(contact)
        contact_spider.contacts_id_dict = prepared_for_get_contact_info
        clients_with_filled_contacts: list[Client] = contact_spider.get_additional_info()
        [self.dao.update(client) for client in clients_with_filled_contacts]
        return clients_with_filled_contacts

    def __run(self):
        "first bot"
        logger.log(user_log_name, f"work first bot")
        new_clients = self.get_new_work_requests()
        saved_new_clients = self.save_new_work_requests(new_clients)
        urls = self.make_url(saved_new_clients)
        "second bot"
        if urls:
            logger.log(user_log_name, f"work second bot")
            additional_info = self.apply_job_request(urls)
            self.update_client_info(additional_info)
        "third bot"
        logger.log(user_log_name, f"work third bot")
        clients_need_email = self.get_contact_info()
        if clients_need_email:
            send_email(clients_need_email)
        logger.log(user_log_name, f"third bot is done")

    def run(self):
        try:
            self.__run()
        except PageDoesNotOpen:
            logger.log(user_log_name, f"The page with the vacancy does not open and the elements were not found")
        except NoSuchElementError as e:
            logger.log(user_log_name, f"{e}")
        except requests.exceptions.RequestException as e:
            logger.log(user_log_name, f" problem with proxy or connection: {e}")
        except Exception as e:
            logger.log(user_log_name, f"{e}")
        finally:
            logger.log(user_log_name, f"Work is done")
