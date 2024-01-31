from django.contrib import admin

from chat_control.models import StoredEmail, Message

# Register your models here.
admin.site.register(StoredEmail)
admin.site.register(Message)
