from django.contrib.auth.models import AbstractUser
from django.db import models


class AppUser(AbstractUser):
    REQUIRED_FIELDS = ['email']

    organisation_name = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = 'App User'
        verbose_name_plural = 'App Users'