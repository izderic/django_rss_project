from django.shortcuts import render
from django.views.generic import CreateView
from django.urls import reverse
from django.http import HttpResponseRedirect, JsonResponse
from django.core.paginator import Paginator
from django.core.management import call_command

from .forms import CreateFeedForm, FeedFormSet
from .models import Feed, Word, WordType


def home(request):
    """
    Main view. Contains links to feeds page and words page.
    """
    return render(request, 'home.html')


def feed_list(request):
    """
    Displays the list of feeds and enables feed status change.
    """
    if request.method == "GET":
        initial = [{'url': feed.url, 'active': feed.active} for feed in Feed.objects.all()]
        return render(request, 'rss/feed_list.html', {
            'formset': FeedFormSet(initial=initial)
        })
    elif request.method == "POST":
        formset = FeedFormSet(request.POST)
        for form in formset.forms:
            if form.is_valid():
                url = form.cleaned_data['url']
                active = form.cleaned_data['active']
                feed = Feed.objects.get(url=url)
                if feed.active is not active:
                    feed.active = active
                    feed.save()

        return HttpResponseRedirect(reverse('rss:feed_list'))


def word_list(request):
    """
    Renders the list of words.
    """
    feeds = Feed.objects.active_feeds().order_by('url')
    return render(request, 'rss/word_list.html', {'feeds': feeds})


def get_words(request):
    """
    Returns data for the table in word_list view.
    """
    limit = int(request.GET.get('limit'))
    offset = int(request.GET.get('offset'))
    feed_id = request.GET.get('feed_id')

    page_size = limit
    page_number = 1 + offset / page_size

    if feed_id:
        items = WordType.objects.filter(content_type__model='feed', object_id=feed_id).select_related('word').order_by('-number', 'word__word')
    else:
        items = Word.objects.all().select_related().order_by('-number', 'word')

    search = request.GET.get('search', None)
    if search:
        if feed_id:
            items = items.filter(word__word__icontains=search)
        else:
            items = items.filter(word__icontains=search)

    total = items.count()
    paginator = Paginator(items, page_size)
    objects = paginator.page(page_number)

    rows = [
        {
            'word': item.word.word if feed_id else item.word,
            'number': item.number
        } for item in objects
    ]

    return JsonResponse({'rows': rows, 'total': total})


class CreateFeedView(CreateView):
    """
    View class that provides form for creating the feed.
    """
    template_name = "rss/create_feed.html"
    form_class = CreateFeedForm

    def form_valid(self, form):
        """
        Called when form is valid.
        """
        form.save()
        return super(CreateFeedView, self).form_valid(form)

    def get_success_url(self):
        """
        Redirect to the feed_list page after success.
        """
        return reverse('rss:feed_list')


def save_feed_data(request):
    """
    Calls the management command.
    """
    call_command('save_feed_data')
    return HttpResponseRedirect(reverse('home'))
