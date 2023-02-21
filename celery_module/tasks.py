import pytz

from celery_module.celery_app import app
from config import TIMEZONE
from task_manager_module.task_manager import TaskManager


@app.task(name='runner_task')
def runner_task():
    manager = TaskManager()
    manager.run()


app.conf.beat_schedule = {
    'scheduled_bot_launch': {
        'task': "runner_task",
        'schedule': 180.0,
    },
}

app.conf.timezone = pytz.timezone(TIMEZONE)
