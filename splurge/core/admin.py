from django.contrib import admin

from .models import AppUser, Employee, Team

admin.site.register(AppUser)
admin.site.register(Employee)
admin.site.register(Team)