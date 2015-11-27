from celery import Celery, shared_task
import requests
from django.conf import settings

from .helpers import send_email

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