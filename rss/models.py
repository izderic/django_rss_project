from django.db import models


class Feed(models.Model):
    """
    The Feed class is defined with url and boolean value of activity.
    """
    url = models.URLField(unique=True)
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.url


class Entry(models.Model):
    """
    The Entry class.
    """
    url = models.URLField(unique=True)
    feed = models.ForeignKey(Feed)
    content = models.TextField(max_length=1024)

    def __unicode__(self):
        return self.url


class Word(models.Model):
    """
    The Word class.
    """
    word = models.CharField(max_length=50, unique=True)
    count = models.IntegerField(default=0)

    def __unicode__(self):
        return self.word
