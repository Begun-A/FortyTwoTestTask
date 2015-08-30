from django.contrib import admin
from hello.models import Contact, LogWebRequest, SignalLog


class LogWebRequestAdmin(admin.ModelAdmin):
    list_display = (
        'priority',
        'method',
        'path',
        'status_code',
        'remote_addr',
        'time'
    )


admin.site.register(Contact)
admin.site.register(LogWebRequest, LogWebRequestAdmin)
admin.site.register(SignalLog)
