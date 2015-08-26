from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from t1_contact.views import ContactView
from t3_requests.views import LogRequestView
from t5_forms.views import LoginView, LogoutView

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', ContactView.as_view(), name='contact'),
    url(r'^requests/$', LogRequestView.as_view(), name='requests'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += staticfiles_urlpatterns()
