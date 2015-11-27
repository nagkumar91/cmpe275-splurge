from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.crypto import get_random_string


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