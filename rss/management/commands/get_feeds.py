from django.core.management.base import BaseCommand, CommandError
from rss.models import Feed

import feedparser


class Command(BaseCommand):
    args = ''
    help = 'Gets the data for active feeds by url, saves the feed entries to the database'

    def handle(self, *args, **options):
        for feed in Feed.objects.filter(active=True):
            feed_xml = feedparser.parse(feed.url)
