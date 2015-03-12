from django.core.management.base import BaseCommand
from django.db import transaction

from rss.models import Feed, Entry, Word, WordType


class Command(BaseCommand):
    args = ''
    help = 'Gets the data for active feeds by url, saves the feed entries to the database'

    @transaction.atomic
    def handle(self, *args, **options):
        """
        Gets the data for active feeds by url, saves the feed entries to the database
        """
        # Delete all previous data first
        WordType.delete_all()
        Word.delete_all()
        Entry.delete_all()

        self.stdout.write('Counting words...')
        entry_data, feed_data, word_data, entry_url_lookup = Word.count_words()
        self.stdout.write('Counting complete.')

        self.stdout.write('Saving data...')
        words = [Word.create(word, number) for word, number in word_data.items()]
        Word.objects.bulk_create(words)

        Entry.objects.bulk_create(entry_url_lookup.values())

        # Lookups used to create WordType objects
        words_lookup = dict(Word.objects.all().values_list('word', 'id'))
        feeds_lookup = {item.id: item for item in Feed.objects.active_feeds()}
        entries_lookup = {item.url: item for item in Entry.objects.all()}

        # Save WordType objects
        feed_word_types = Word.create_word_types(feed_data, feeds_lookup, words_lookup)
        entry_word_types = Word.create_word_types(entry_data, entries_lookup, words_lookup)
        WordType.objects.bulk_create(feed_word_types + entry_word_types)

        self.stdout.write('Complete!')
