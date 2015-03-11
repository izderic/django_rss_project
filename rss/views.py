from django.shortcuts import render
from django.views.generic import CreateView
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from .forms import CreateFeedForm, FeedFormSet
from .models import Feed


def feed_list(request):

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

        return HttpResponseRedirect(reverse('feed_list'))


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
        return reverse('feed_list')