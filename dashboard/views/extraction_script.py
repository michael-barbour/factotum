import math
from random import shuffle
import os
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.forms import ModelForm
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext_lazy as _
from django.core.files import File
from django.core.files.storage import FileSystemStorage

from dashboard.models import (DataGroup, DataDocument, DataSource,
                              ExtractedText, Script, QAGroup, ExtractedChemical)

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

def get_next_or_prev(models, item, direction):
    '''
    Returns the next or previous item of
    a query-set for 'item'.

    'models' is a query-set containing all
    items of which 'item' is a part of.

    direction is 'next' or 'prev'

    '''
    getit = False
    if direction == 'prev':
        models = models.reverse()
    for m in models:
        if getit:
            return m
        if item == m:
            getit = True
    if getit:
        # This would happen when the last
        # item made getit True
        return models[0]
    return False


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
        											'extractedtexts' : texts,
                                                    'qagroup': group})
    # pks of text and docs are the same!
    doc_text_ids = list(ExtractedText.objects.filter(extraction_script=es,
                                                     qa_checked=False
                                                     ).values_list('pk',
                                                                   flat=True))
    qa_group = QAGroup.objects.create(extraction_script=es)
    if len(doc_text_ids) < 100:
        texts = ExtractedText.objects.filter(pk__in=doc_text_ids)
    else:
        random_20 = math.ceil(len(doc_text_ids)/5)
        shuffle(doc_text_ids)  # this is used to make random selection of texts
        texts = ExtractedText.objects.filter(pk__in=doc_text_ids[:random_20])
    for text in texts:
        text.qa_group = qa_group
        text.save()
    es.qa_begun = True
    es.save()
    return render(request, template_name, {'extractionscript'  : es,
											'extractedtexts' : texts,
                                            'qagroup': qa_group})

@login_required()
def extraction_script_detail(request, pk,
                        template_name='extraction_script/extraction_script_detail.html'):
    extractionscript = get_object_or_404(Script, pk=pk)
    data = {}
    data['object_list'] = extractionscript
    return render(request, template_name, data)

@login_required()
def extracted_text_qa(request, pk, template_name='qa/extracted_text_qa.html'):

    extext = ExtractedText.objects.get(pk=pk)
    datadoc = DataDocument.objects.get(pk=pk)
    exscript = extext.extraction_script
    chems = ExtractedChemical.objects.filter(extracted_text=extext)
    # get the next unapproved Extracted Text object
    # Its ID will populate the URL for the "Skip" button
    extextnext = get_next_or_prev(ExtractedText.objects.filter(qa_group=extext.qa_group, qa_checked=False ), extext, 'next')
    if extextnext:
        # Replace our item with the next one
        nextid = extextnext.pk
    if extextnext == extext:
        nextid = 0
    # derive the number of approved records and remaining unapproved ones in the QA Group
    a = extext.qa_group.get_approved_doc_count()
    r = ExtractedText.objects.filter(qa_group=extext.qa_group).count() - a
    stats = '%s document(s) approved, %s documents remaining' % (a, r)
    return render(request, template_name, {'extracted': extext, \
        'doc': datadoc, 'script': exscript, 'chems':chems, 'stats':stats, 'nextid':nextid})
