"""
Defines urls for current app
"""
from django.conf.urls import patterns, url

from rss.views import CreateFeedView


urlpatterns = patterns(
    '',
    url(r'^feed_list/$', 'rss.views.feed_list', name='feed_list'),
    url(r'^word_list/$', 'rss.views.word_list', name='word_list'),
    url(r'^get_words/$', 'rss.views.get_words', name='get_words'),
    url(r'^save_feed_data/$', 'rss.views.save_feed_data', name='save_feed_data'),
    url(r'^create_feed/', CreateFeedView.as_view(), name='create_feed'),
)