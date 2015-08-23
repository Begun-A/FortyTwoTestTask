from django.conf.urls import patterns, include, url

from django.contrib import admin
from hello.views import ContactView
admin.autodiscover()

urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^$', 'fortytwo_test_task.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^contact/(?P<pk>\d+)/$', ContactView.as_view(), name='contact'),
    url(r'^admin/', include(admin.site.urls)),
)
