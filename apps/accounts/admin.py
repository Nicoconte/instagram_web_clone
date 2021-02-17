from django.contrib import admin

from .models import Account, Follower


admin.site.register(Account)
admin.site.register(Follower)

