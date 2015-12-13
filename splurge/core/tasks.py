from celery import Celery, shared_task
import requests
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.template import Context
from django.template.loader import get_template
import datetime
from django.utils import timezone

# from .helpers import send_email, send_complex_message, send_claimed_email_to_employer

app = Celery('core')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


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


@shared_task
def activation_mail_queue(app_user):
    body = "Click here to activate your account! %s/activate_user/%s" % (settings.SITE_URL, app_user.unique_code)
    to = app_user.email
    subject = "Splurge activate account"
    from_id = "noreply@getsplurge.com"
    send_email(to, subject, body, from_id)


@shared_task
def gift_card(app_user, employee, gift_card):
    html = get_template("email_new_gc.html").render(Context({
        "employee": employee,
        "appuser": app_user,
        "card": gift_card,
    }))
    subject = "Splurge %s" % gift_card.unique_code
    send_complex_message(employee.email_id, subject, html)


from .models import GiftCard


@shared_task
def _send_complex_message(to, subject, body):
    send_complex_message(to, subject, body)


@app.task(bind=True)
def check_for_expiring_cards(self, *args, **kwargs):
    print "Checking for expiring cards"
    now = datetime.datetime.now()
    gc_objects = GiftCard.objects.filter(
        expiry_timestamp__range=(timezone.make_aware(now), timezone.make_aware(now + datetime.timedelta(days=1))),
        expired=False, expiry_reminder=False
    )
    for gc in gc_objects:
        html = get_template("email_gc_will_expire_soon.html").render(Context({
            "employee": gc.to,
            "appuser": gc.given_by,
            "card": gc
        }))
        subject = "Splurge %s" % gc.unique_code
        _send_complex_message.delay(gc.to.email_id, subject, html)
        gc.expiry_reminder = True
        gc.save()


@app.task(bind=True)
def check_for_expired_cards(self, *args, **kwargs):
    print "Checking for expired cards"
    now = datetime.datetime.now()
    gc_objects = GiftCard.objects.filter(
        expiry_timestamp__range=(timezone.make_aware(now), timezone.make_aware(now + datetime.timedelta(minutes=4))),
        expired=False
    )
    for gc in gc_objects:
        html = get_template("email_gift_card_expired_employee.html").render(Context({
            "employee": gc.to,
            "appuser": gc.given_by,
            "card": gc
        }))
        subject = "Splurge card expired!"
        _send_complex_message.delay(gc.to.email_id, subject, html)
        gc.expired = True
        gc.save()
        html = get_template("email_gift_card_expired_appuser.html").render(Context({
            "employee": gc.to,
            "appuser": gc.given_by,
            "card": gc,
            "returned_amount": (0.75 * gc.amount)
        }))
        gc.given_by.balance += 0.75 * gc.amount
        gc.save()
        _send_complex_message.delay(gc.given_by.email, subject, html)


@shared_task
def fetch_mail_from_context_io():
    print "received an email with subject. So fetch from context.io and mark the card as used"
    url = "https://api.context.io/2.0/accounts/%s/messages?include_body=1&subject=%2FSplurge%2A%2F" % settings.CONTEXT_IO_ACCOUNT_ID
    r = requests.get(url)
    if r.status_code == '200':
        now = datetime.datetime.now()
        lim = now - datetime.timedelta(minutes=30)
        for m in r.json():
            m_date = datetime.datetime.fromtimestamp(int(m['date_received']))
            if (now > m_date) and (lim < m_date):
                subj = m['subject']
                subj = subj.replace("Splurge ", "")
                try:
                    splurge_card = GiftCard.objects.get(unique_code=subj)
                    splurge_card.claimed = True
                    send_claimed_email_to_employer(splurge_card)
                    send_claimed_email_to_employee(splurge_card)
                except ObjectDoesNotExist:
                    pass
