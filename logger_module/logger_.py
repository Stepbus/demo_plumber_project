import datetime as dt
import os

from loguru import logger
import pytz

from config import TIMEZONE

timezone = TIMEZONE
user_log_name = 'BOT'
user_log = logger.level(name=user_log_name, no=25, color="<blue>", icon="@")
user_log_format = '{extra[datetime]} | {message}'
system_log_format = '{time} {level} {message}'


def set_datetime(record):
    record["extra"]["datetime"] = dt.datetime.now(tz=pytz.timezone(timezone)).strftime('%d-%m-%Y %H:%M:%S')


def get_paths():
    cwd_path = os.getcwd()
    if cwd_path.split('/')[-1] not in ('ben_allal', 'app'):
        logger_path_info = '../logs/info.log'
        logger_path_error = '../logs/error.log'
        logger_path_user = '../logs/user.log'
    else:
        logger_path_info = 'logs/info.log'
        logger_path_error = 'logs/error.log'
        logger_path_user = 'logs/user.log'
    return logger_path_info, logger_path_error, logger_path_user


logger_path_info, logger_path_error, logger_path_user = get_paths()

logger.configure(patcher=set_datetime)
logger.add(logger_path_info, format=system_log_format, level='INFO', rotation='10 MB', compression='zip',
           retention='1 month')
logger.add(logger_path_error, format=system_log_format, level='ERROR', rotation='10 MB', compression='zip',
           retention='1 month')
logger.add(logger_path_user, format=user_log_format, level=user_log_name, rotation='10 MB', compression='zip',
           retention='1 month')
