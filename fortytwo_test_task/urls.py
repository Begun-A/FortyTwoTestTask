from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from hello.views import (
    ContactView,
    LogRequestView,
    LoginView,
    LogoutView,
)

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', ContactView.as_view(), name='contact'),
    url(r'^requests/$', LogRequestView.as_view(), name='requests'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^admin/', include(admin.site.urls)),

) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()
