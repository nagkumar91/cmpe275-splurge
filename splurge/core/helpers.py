import random
import string
import requests
from django.conf import settings
from django.template import Context
from django.template.loader import get_template

from .tasks import fetch_mail_from_context_io, activation_mail_queue


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


def _fetch_mail_from_context_io():
    fetch_mail_from_context_io.delay()


def _activation_mail_queue(appuser):
    activation_mail_queue.delay(appuser)


def send_claimed_email_to_employer(splurge_card):
    to = splurge_card.given_by.email
    subject = "Splurge card claimed"
    html = get_template("email_redeemed_gc.html").render(Context({
        "employee": splurge_card.to,
        "appuser": splurge_card.given_by,
        "card": splurge_card
    }))
    return requests.post(
        settings.MAILGUN_API_URL,
        auth=("api", settings.MAILGUN_SECRET_KEY),
        data={"from": "Splurge <nagkumar91@gmail.com>",
              "to": to,
              "subject": subject,
              # "text": "Testing some Mailgun awesomness!",
              "html": html})


def send_claimed_email_to_employee(splurge_card):
    to = splurge_card.to.email_id
    subject = "Splurge card claimed"
    html = get_template("email_claim_successful.html").render(Context({
        "employee": splurge_card.to,
        "appuser": splurge_card.given_by,
        "card": splurge_card
    }))
    return requests.post(
        settings.MAILGUN_API_URL,
        auth=("api", settings.MAILGUN_SECRET_KEY),
        data={"from": "Splurge <nagkumar91@gmail.com>",
              "to": to,
              "subject": subject,
              # "text": "Testing some Mailgun awesomness!",
              "html": html})
