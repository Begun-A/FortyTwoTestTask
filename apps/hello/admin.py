from django.contrib import admin
from hello.models import Contact, LogWebRequest, SignalLog


class LogWebRequestAdmin(admin.ModelAdmin):
    list_filter = ('priority',)


admin.site.register(Contact)
admin.site.register(LogWebRequest, LogWebRequestAdmin)
admin.site.register(SignalLog)
