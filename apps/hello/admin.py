from django.contrib import admin
from .models import Contact, LogWebRequest

admin.site.register(Contact)
admin.site.register(LogWebRequest)
