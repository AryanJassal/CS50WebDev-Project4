from django.contrib import admin

from .models import User, Posts, Following, Like

admin.site.register(User)
admin.site.register(Posts)
admin.site.register(Following)
admin.site.register(Like)
