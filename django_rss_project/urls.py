from django.conf.urls import patterns, include, url
from django.contrib import admin

from rss.api import WordResource


urlpatterns = patterns(
    '',
    url(r'^$', 'rss.views.home', name='home'),
    url(r'^rss/', include('rss.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^word/', WordResource.as_view()),
)
