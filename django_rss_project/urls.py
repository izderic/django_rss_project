from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'django_rss_project.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^rss/', include('rss.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
