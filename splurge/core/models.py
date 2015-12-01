import datetime
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.crypto import get_random_string
from model_utils.models import TimeStampedModel


class AppUser(AbstractUser):
    REQUIRED_FIELDS = ['email']

    organisation_name = models.CharField(max_length=255, null=True, blank=True)
    unique_code = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = 'App User'
        verbose_name_plural = 'App Users'

    def save(self, *args, **kwargs):
        if not self.unique_code:
            self.unique_code = get_random_string(length=25)
        super(AppUser, self).save(*args, **kwargs)


class Employee(TimeStampedModel):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email_id = models.EmailField()
    phone_number = models.CharField(max_length=15)
    app_user = models.ForeignKey(AppUser, related_name='employees')
    team = models.ForeignKey('Team', related_name='employees', null=True, blank=True)

    class Meta:
        verbose_name = 'Employee'
        verbose_name_plural = 'Employees'

    def __unicode__(self):
        return "%s %s" % (self.first_name, self.last_name)


class Team(TimeStampedModel):
    name = models.CharField(max_length=255)
    app_user = models.ForeignKey(AppUser, related_name='teams')

    class Meta:
        verbose_name_plural = 'Teams'
        verbose_name = 'Team'

    def __unicode__(self):
        return "%s - %s" % (self.name, self.app_user.organisation_name)


class GiftCard(TimeStampedModel):
    amount = models.IntegerField(default=0)
    given_by = models.ForeignKey(AppUser, related_name='gift_cards')
    to = models.ForeignKey(Employee, related_name='gift_cards')
    expired = models.BooleanField(default=False)
    claimed = models.BooleanField(default=False)
    expiry_timestamp = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'Gift Card'
        verbose_name_plural = 'Gift Cards'

    def __unicode__(self):
        return "%s %s" % (self.amount, self.given_by)

    def save(self, *args, **kwargs):
        if not self.expired:
            if not self.expiry_timestamp:
                self.expiry_timestamp = self.created + datetime.timedelta(days=2)
        super(GiftCard, self).save(*args, **kwargs)