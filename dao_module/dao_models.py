from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy_utils import EmailType, URLType

from dao_module.connection import Base


class KeyWords(Base):
    __tablename__ = 'KeyWords'

    key_words = Column("KeyWords", String(200), primary_key=True)

    def __init__(self, key_words):
        super().__init__()
        self.key_words = key_words

    def __repr__(self):
        return f"{self.key_words}"


class IgnoreWords(Base):
    __tablename__ = 'IgnoreWords'

    key_ignore = Column("IgnoreWords", String(200), primary_key=True)

    def __init__(self, key_ignore):
        super().__init__()
        self.key_ignore = key_ignore

    def __repr__(self):
        return f"{self.key_ignore}"


class Client(Base):
    __tablename__ = 'Clients'

    client_id = Column("ClientId", Integer, primary_key=True)
    job_title = Column("Job title", String(200), nullable=True)
    date_published = Column("PublishedDate", DateTime, nullable=True)
    job_location = Column("Job location", String(200), nullable=True)
    type_klus = Column("Type klus", String(400), nullable=True)
    soort_probleem = Column("Soort probleem", String(400), nullable=True)
    aanvullende_informatie = Column("Aanvullende informatie", String(700), nullable=True)
    contact_name = Column("Contact name", String(100), nullable=True)
    contact_email = Column("Contact email", EmailType(length=254), nullable=True)
    contact_phone = Column("Contact phone", String(20), nullable=True)
    client_url = Column("Url address", URLType, nullable=True)

    def __init__(self, client_id, job_title, date_published, job_location, type_klus=None, soort_probleem=None,
                 aanvullende_informatie=None, contact_name=None, contact_email=None, contact_phone=None,
                 client_url=None):
        super().__init__()
        self.client_id = client_id
        self.job_title = job_title
        self.date_published = date_published
        self.job_location = job_location
        self.type_klus = type_klus
        self.soort_probleem = soort_probleem
        self.aanvullende_informatie = aanvullende_informatie
        self.contact_name = contact_name
        self.contact_email = contact_email
        self.contact_phone = contact_phone
        self.client_url = client_url

    def as_dict(self):
        as_dict = {key: getattr(self, key) for key in self.__dict__.keys() if not key.startswith('_')}
        return as_dict

    def __repr__(self):
        return f"{self.client_id} {self.job_title} {self.date_published} {self.job_location}"
