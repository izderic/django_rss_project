from django.urls import path, include
from django.contrib import admin

from rss.api import WordResource
from rss.views import home


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('rss/', include('rss.urls', namespace='rss')),
    path('word/', WordResource.as_view()),
]
