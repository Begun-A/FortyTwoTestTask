from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from hello.views import (
    ContactView,
    LogRequestView,
    LoginView
)
admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', ContactView.as_view(), name='contact'),
    url(r'^requests/$', LogRequestView.as_view(), name='requests'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += staticfiles_urlpatterns()
