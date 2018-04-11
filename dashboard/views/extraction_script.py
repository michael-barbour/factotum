import math
from random import shuffle

from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.forms import ModelForm
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext_lazy as _
from django.core.files import File
from django.core.files.storage import FileSystemStorage

from dashboard.models import (DataGroup, DataDocument, DataSource,
                              ExtractedText, Script, QAGroup)

class ExtractionScriptForm(ModelForm):
    required_css_class = 'required' # adds to label tag
    class Meta:
        model = Script
        fields = ['title', 'url', 'qa_begun']
        labels = {
            'qa_begun': _('QA has begun'),
            }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(ExtractionScriptForm, self).__init__(*args, **kwargs)

@login_required()
def extraction_script_list(request, template_name='qa/extraction_script_list.html'):

    extractionscript = Script.objects.filter(script_type='EX')
    data = {}
    data['object_list'] = extractionscript
    return render(request, template_name, data)

@login_required()
def extraction_script_qa(request, pk,
                        template_name='qa/extraction_script.html'):
    es = get_object_or_404(Script, pk=pk)
    if es.qa_begun:
        # has qa begun and not complete? if both T, return group to be finished
        if QAGroup.objects.filter(extraction_script=es,
                                  qa_complete=False).exists():
            # return docs that are in extracted texts QA group
            group = QAGroup.objects.get(extraction_script=es,
                                            qa_complete=False)
            print(group)
            texts = ExtractedText.objects.filter(qa_group=group,
                                                 qa_checked=False)
            return render(request, template_name, {'extractionscript'  : es,
        											'extractedtexts' : texts})
    # pks of text and docs are the same!
    doc_text_ids = ExtractedText.objects.filter(extraction_script=pk)
    doc_text_ids = list(ExtractedText.objects.filter(extraction_script=es,
                                                     qa_checked=False
                                                     ).values_list('pk',
                                                                   flat=True))
    random_20 = math.ceil(len(doc_text_ids)/5)
    shuffle(doc_text_ids)  # this is used to make random selection of texts
    qa_group = QAGroup.objects.create(extraction_script=es)
    texts = ExtractedText.objects.filter(pk__in=doc_text_ids[:random_20])
    for text in texts:
        text.qa_group = qa_group
        text.save()
    es.qa_begun = True
    es.save()
    return render(request, template_name, {'extractionscript'  : es,
											'extractedtexts' : texts})

@login_required()
def extraction_script_detail(request, pk,
                        template_name='extraction_script/extraction_script_detail.html'):
    extractionscript = get_object_or_404(Script, pk=pk)
    data = {}
    data['object_list'] = extractionscript
    return render(request, template_name, data)
