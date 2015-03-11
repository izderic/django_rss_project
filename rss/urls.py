"""
Defines urls for current app
"""
from django.conf.urls import patterns, url

from rss.views import CreateFeedView


urlpatterns = patterns(
    '',
    url(r'^feed_list/$', 'rss.views.feed_list', name='feed_list'),
    url(r'^create_feed/', CreateFeedView.as_view(), name='create_feed'),
)