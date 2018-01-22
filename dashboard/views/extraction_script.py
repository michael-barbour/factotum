from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.forms import ModelForm
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext_lazy as _
from django.core.files import File
from django.core.files.storage import FileSystemStorage

from dashboard.views import *
from dashboard.models import DataGroup, DataDocument, DataSource, ExtractedText

class ExtractionScriptForm(ModelForm):
    required_css_class = 'required' # adds to label tag
    class Meta:
        model = ExtractionScript
        fields = ['title', 'url', 'qa_begun']
        labels = {
            'qa_begun': _('QA has begun'),
            }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(ExtractionScriptForm, self).__init__(*args, **kwargs)

@login_required()
def extraction_script_list(request, template_name='qa/extraction_script_list.html'):

    extractionscript = ExtractionScript.objects.all()
    data = {}
    data['object_list'] = extractionscript
    return render(request, template_name, data)

@login_required()
def extraction_script_qa(request, pk,
                        template_name='qa/extraction_script.html'):
    es = get_object_or_404(ExtractionScript, pk=pk)
    ets = ExtractedText.objects.filter(extraction_script=pk)
    return render(request, template_name, {'extractionscript'  : es,
											'extractedtexts' : ets})

@login_required()
def extraction_script_detail(request, pk,
                        template_name='extraction_script/extraction_script_detail.html'):
    extractionscript = get_object_or_404(ExtractionScript, pk=pk)
    data = {}
    data['object_list'] = extractionscript
    return render(request, template_name, data)
