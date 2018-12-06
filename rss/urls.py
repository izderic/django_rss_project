"""
Defines urls for current app
"""
from django.urls import  path

from rss import views

app_name = 'rss'
urlpatterns = [
    path('feed_list/', views.feed_list, name='feed_list'),
    path('word_list/', views.word_list, name='word_list'),
    path('get_words/', views.get_words, name='get_words'),
    path('save_feed_data/', views.save_feed_data, name='save_feed_data'),
    path('create_feed/', views.CreateFeedView.as_view(), name='create_feed'),
]
