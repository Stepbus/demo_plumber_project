from typing import Type

from sqlalchemy.orm import sessionmaker

from dao_module.connection import engine, Base
from dao_module.dao_models import KeyWords, Client, IgnoreWords


class Dao:

    def __init__(self):
        session = sessionmaker(engine)
        self.session = session()
        Base.metadata.create_all(engine)

    def create_one(self, instance: Client | KeyWords):
        match instance:
            case Client():
                selector = {"client_id": instance.client_id}
            case KeyWords():
                selector = {"key_words": instance.key_words}
            case IgnoreWords():
                selector = {"key_ignore": instance.key_ignore}
            case _:
                selector = {}
        if not self.session.query(instance.__class__).filter_by(**selector).first():
            self.session.add(instance)
            self.session.commit()
            return instance

    def create_all(self, data_list: list[Client | KeyWords]) -> list:
        list_of_saved_instances = [self.create_one(instance) for instance in data_list]
        list_of_new_instances = [instance for instance in list_of_saved_instances if instance]
        return list_of_new_instances

    def get_all(self, table) -> list:
        result = self.session.query(table)
        all_data_list = [unit for unit in result]
        return all_data_list

    def get_by_field(self, table, field: dict):
        result = self.session.query(table).filter_by(**field).all()
        return result

    def select_clients_fields_by_id(self, client_id):
        result = self.session.query(Client.contact_name, Client.contact_email, Client.contact_phone).filter_by(
            client_id=client_id).first()
        return result

    def update(self, instance: Client):
        self.session.query(instance.__class__).filter_by(client_id=instance.client_id).update(
            instance.as_dict())
        self.session.commit()

    def get_last_record(self, cls_instance: Type[Client]) -> Client:
        return self.session.query(cls_instance).order_by(cls_instance.date_published.desc()).first()
