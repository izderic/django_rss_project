from django.http import JsonResponse, HttpResponse
from django.views.generic import View
from django.core.exceptions import ObjectDoesNotExist
from django.core import serializers

from .models import Word, WordType, Feed, Entry


class WordResource(View):
    """
    Simple JSON API using the class based view.
    """
    model = Word

    def get(self, request):
        """
        Returns the number of occurrences of the specified word in the feed, entry or total.
        """
        word = request.GET.get('word')
        feed_url = request.GET.get('feed_url')
        entry_url = request.GET.get('entry_url')

        if word:
            if not (feed_url or entry_url):
                try:
                    word_obj = self.model.objects.get(word=word)
                    return JsonResponse(word_obj.number, safe=False)
                except ObjectDoesNotExist:
                    return JsonResponse('Word "%s" does not exist.' % word)
            elif feed_url:
                return self.num_of_occurrences(word, Feed, feed_url)
            elif entry_url:
                return self.num_of_occurrences(word, Entry, entry_url)
        else:
            return HttpResponse(serializers.serialize('json', self.model.objects.all()))

    def num_of_occurrences(self, word, model, url):
        """
        Returns the number of occurrences of the word in feed or entry.
        """
        class_string = model.class_string()
        try:
            obj = model.objects.get(url=url)
            word_type_obj = WordType.objects.get(content_type__model=class_string.lower(), word__word=word, object_id=obj.id)
            return JsonResponse(word_type_obj.number, safe=False)
        except model.DoesNotExist:
            return HttpResponse('%s with URL %s does not exist.' % (class_string, url))
        except WordType.DoesNotExist:
            return HttpResponse('Word "%s" does not exist in %s %s.' % (word, class_string.lower(), url))
