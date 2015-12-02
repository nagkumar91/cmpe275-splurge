from celery import Celery, shared_task
import requests
from django.conf import settings
from django.template import Context
from django.template.loader import get_template

from .helpers import send_email, send_complex_message

app = Celery('core')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

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
    print html
    subject = "Splurge %s" % gift_card.unique_code
    send_complex_message(employee.email_id, subject, html)