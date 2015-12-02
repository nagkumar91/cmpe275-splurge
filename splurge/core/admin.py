from django.contrib import admin
from .models import AppUser, Employee, Team, GiftCard, GiftCardCategory, GiftCardRedeemableSite

admin.site.register(AppUser)
admin.site.register(Employee)
admin.site.register(Team)
admin.site.register(GiftCard)
admin.site.register(GiftCardCategory)
admin.site.register(GiftCardRedeemableSite)
