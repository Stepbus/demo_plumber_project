from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

from config import POSTGRES_CONNECTION_STR
engine = create_engine(POSTGRES_CONNECTION_STR)
Base = declarative_base()
