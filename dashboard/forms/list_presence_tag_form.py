from django import forms
from dashboard.models import ExtractedListPresence
from dal import autocomplete


class ExtractedListPresenceTagForm(autocomplete.FutureModelForm):

    class Meta:
        model = ExtractedListPresence
        fields = ['tags']

        widgets = {
            'tags': autocomplete.TaggitSelect2(
                'list_presence_tags_autocomplete')
        }

    def __init__(self, *args, **kwargs):
        super(ExtractedListPresenceTagForm, self).__init__(*args, **kwargs)
        self.fields['tags'].widget.attrs.update({'class':'mr-2 ml-2',
                                                 'style':'width:60%',
                                                 'data-minimum-input-length': 3})
        self.fields['tags'].label = 'List Presence Keywords'
        self.fields['tags'].help_text = ''
