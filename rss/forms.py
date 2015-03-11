from django.forms import ModelForm, Form, BooleanField, URLField
from django.forms.formsets import formset_factory

from .models import Feed


class CreateFeedForm(ModelForm):
    """
    Form for creating new Feed and editing existing.
    """
    class Meta:
        model = Feed
        fields = ('url', 'active')

    def __init__(self, **kwargs):
        super(CreateFeedForm, self).__init__(**kwargs)
        self.fields['url'].widget.attrs['class'] = 'form-control'


class RowFeedForm(Form):
    """
    Form used in formset to change the state of the feed.
    """
    url = URLField()
    active = BooleanField(required=False)

    def __init__(self, **kwargs):
        super(RowFeedForm, self).__init__(**kwargs)
        attributes = {
            'readonly': True,
            'class': 'url'
        }
        self.fields['url'].widget.attrs.update(attributes)


FeedFormSet = formset_factory(RowFeedForm, extra=0)
