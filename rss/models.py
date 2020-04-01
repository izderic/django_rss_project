import re
import feedparser
import ssl
from collections import Counter

from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.html import strip_tags

if hasattr(ssl, '_create_unverified_context'):
    ssl._create_default_https_context = ssl._create_unverified_context


class Base(models.Model):
    """
    Base abstract class for models.
    """
    class Meta:
        abstract = True

    @classmethod
    def delete_all(cls):
        """
        Deletes all records from database.
        Limited to 999 because of SQLite3.
        """
        while cls.objects.count():
            ids = cls.objects.values_list('pk', flat=True)[:999]
            cls.objects.filter(pk__in = ids).delete()


class FeedManager(models.Manager):
    """
    Custom Manager for feeds.
    """
    def active_feeds(self):
        return self.get_queryset().filter(active=True)


class Feed(Base):
    """
    The Feed class is defined with url and boolean value of activity.
    """
    url = models.URLField(unique=True)
    active = models.BooleanField(default=True)
    objects = FeedManager()

    @classmethod
    def class_string(cls):
        return 'Feed'

    def __str__(self):
        return self.url


class Entry(Base):
    """
    The Entry class. URL is unique.
    """
    url = models.URLField(unique=True)
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE)
    content = models.TextField(max_length=1024)

    @classmethod
    def create(cls, url, feed, content):
        entry = cls(url=url, feed=feed, content=content)
        return entry

    @classmethod
    def class_string(cls):
        return 'Entry'

    def __str__(self):
        return self.url


class Word(Base):
    """
    The Word class. Number is the overall number of occurrences.
    """
    word = models.CharField(max_length=50, unique=True)
    number = models.IntegerField(default=1)

    @classmethod
    def create(cls, word, number):
        word = cls(word=word, number=number)
        return word

    @classmethod
    def count_words(cls):
        """
        Counts the words for feeds, entries and overall.
        """
        feed_data = {}
        entry_data = {}
        entry_url_lookup = {}
        all_words = []

        for feed in Feed.objects.active_feeds():
            parsed_feed = feedparser.parse(feed.url)

            if not parsed_feed.entries:
                continue

            feed_words = []

            for feed_entry in parsed_feed.entries:
                entry_url = feed_entry.link
                content = strip_tags(feed_entry.summary)

                entry_item = entry_url_lookup.get(entry_url)
                if not entry_item:
                    entry_url_lookup.update({entry_url: Entry.create(entry_url, feed, content)})

                words = re.findall('\w+', content, re.UNICODE)
                feed_words.extend(words)
                all_words.extend(words)

                entry_data.update({entry_url: Counter(words)})
            feed_data.update({feed.id: Counter(feed_words)})
        word_data = Counter(all_words)

        return entry_data, feed_data, word_data, entry_url_lookup

    @classmethod
    def create_word_types(cls, data, obj_lookup, words_lookup):
        """
        Return the list of the word-feed or word-entry relation objects to save.
        """
        word_types = []
        for obj_id, words in data.items():
            obj = obj_lookup.get(obj_id)
            for word, number in words.items():
                word_type = WordType.create(words_lookup.get(word), obj.id, obj, number)
                word_types.append(word_type)
        return word_types

    def __str__(self):
        return self.word


class WordType(Base):
    """
    Defines the relation of word and any other model.
    Number is the number of occurrences for the specifed object.
    """
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    number = models.IntegerField(default=0)

    @classmethod
    def create(cls, word_id, object_id, content_object, number):
        word_type = cls(word_id=word_id, object_id=object_id, content_object=content_object, number=number)
        return word_type

    class Meta:
        unique_together = (('content_type', 'object_id', 'word'),)

    def __str__(self):
        return '%s - %s' % (self.word.word, self.content_object.url)
