import os

from sendgrid import Mail, SendGridAPIClient

from dao_module.dao_models import Client

from dotenv import load_dotenv

from logger_module.logger_ import logger, user_log_name
from email_notification_module.templates import title, html_cont

load_dotenv()

api_client = os.environ.get('SENDGRID_API_KEY')
from_email = os.environ.get('FROM_EMAIL')
to_email = os.environ.get('TO_EMAIL')
title = title
html_cont = html_cont


def create_html_content(clients: list[Client], list_body, content) -> str:
    for client in clients:
        list_body += content.format(client.job_title, client.type_klus, client.soort_probleem,
                                    client.aanvullende_informatie, client.job_location, client.contact_name,
                                    client.contact_email, client.contact_phone, client.client_url, client.client_url)
    return list_body


def send_email(clients: list[Client]):
    logger.log(user_log_name, f"Sending email ...")
    message = Mail(
        from_email=from_email,
        to_emails=to_email,
        subject='app',
        html_content=create_html_content(clients, title, html_cont)
    )
    try:
        sg = SendGridAPIClient(api_client)
        response = sg.send(message)
        logger.log(user_log_name, f"Sent email with status code {response.status_code}")
    except Exception as e:
        logger.log(user_log_name, f"{e}")
