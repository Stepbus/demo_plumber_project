import os
from dotenv import load_dotenv

load_dotenv()

# postgres connection
POSTGRES_CONNECTION_STR = 'postgresql://{}:{}@{}:{}/{}'.format(
    os.environ.get('POSTGRES_USER'), os.environ.get('POSTGRES_PASSWORD'), os.environ.get('POSTGRES_HOST'),
    os.environ.get('POSTGRES_PORT'), os.environ.get('POSTGRES_DB'))

# rabbitmq connection
BROKER_URL = 'amqp://{}:{}@{}:5672//'.format(os.environ.get('RABBITMQ_USER'), os.environ.get('RABBITMQ_PASS'),
                                             os.environ.get('RABBITMQ_HOST'))

TIMEZONE = "Europe/Amsterdam"
