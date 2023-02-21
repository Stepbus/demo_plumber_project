from celery import Celery

from config import BROKER_URL

broker = BROKER_URL

app = Celery(
    'celery_module',
    broker=broker,
    include=['celery_module.tasks'],
    backend='db+sqlite:///results.db',
)
