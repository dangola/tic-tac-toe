from django.contrib import admin
from .models import Game
from django.contrib.auth.models import User
# Register your models here.
admin.site.register(Game)
# admin.site.register(User)
if admin.site.is_registered(User):
    admin.site.unregister(User)

# admin.site.register(User)
