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
