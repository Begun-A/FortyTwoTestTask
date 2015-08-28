from django.contrib import admin
from hello.models import Contact, LogWebRequest, SignalLog

admin.site.register(Contact)
admin.site.register(LogWebRequest)
admin.site.register(SignalLog)
