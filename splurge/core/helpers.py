import random
import string

import requests
from django.conf import settings


def send_email(to, subject, body, from_id):
    requests.post(
        settings.MAILGUN_API_URL,
        auth=("api", settings.MAILGUN_SECRET_KEY),
        data={"from": from_id,
              "to": [to],
              "subject": subject,
              "text": body})


def send_complex_message(to, subject, body):
    return requests.post(
        settings.MAILGUN_API_URL,
        auth=("api", settings.MAILGUN_SECRET_KEY),
        data={"from": "Splurge <nagkumar91@gmail.com>",
              "to": to,
              "subject": subject,
              # "text": "Testing some Mailgun awesomness!",
              "html": body})



