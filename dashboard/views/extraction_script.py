import math
from random import shuffle
import os
from datetime import datetime
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.forms import ModelForm, Form, BaseInlineFormSet, inlineformset_factory, TextInput, CharField, Textarea, HiddenInput, ValidationError

from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext_lazy as _
from django.core.files import File
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect
from django.urls import reverse

from dashboard.models import (DataGroup, DataDocument, DataSource,
                              ExtractedText, Script, QAGroup, ExtractedChemical)


class ExtractionScriptForm(ModelForm):
    required_css_class = 'required'  # adds to label tag

    class Meta:
        model = Script
        fields = ['title', 'url', 'qa_begun']
        labels = {
            'qa_begun': _('QA has begun'),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(ExtractionScriptForm, self).__init__(*args, **kwargs)

class ExtractedTextForm(ModelForm):

    class Meta:
        model = ExtractedText
        fields = ['record_type','prod_name', 'doc_date', 'rev_num']

    def __init__(self, *args, **kwargs):
        initial_vals = kwargs.get('initial', None)
        super(ExtractedTextForm, self).__init__(*args, **kwargs )
        # The kwarg values are not ending up in the form, though
        kwargs.update(initial=initial_vals)

class QANotesForm(ModelForm):

    class Meta:
        model = ExtractedText
        fields = ['record_type','prod_name', 'doc_date', 'rev_num',
                    'qa_notes', ]
        widgets = {
            'qa_notes' : Textarea,
        }
        labels = {
            'qa_notes': _('QA Notes (required if approving edited records)'),
        }

    def clean(self):
        print('------inside the QANotesForm class clean() method')
        print(self.cleaned_data)
        qa_notes = self.cleaned_data.get('qa_notes')
        qa_edited = self.cleaned_data.get('qa_edited')

        if qa_edited and (qa_notes is None or qa_notes == ''):
            raise ValidationError('qa_notes needs to be populated if you edited the data')

        return self.cleaned_data

    def __init__(self, *args, **kwargs):
        initial_vals={}
        print('kwargs:')
        print(kwargs)
        # These arguments hold the qa_attributes when the form is being approved:
        if kwargs.get('initial', None) is not None:
            initial_vals = kwargs.get('initial', None)
            print('----kwargs initial dict at beginning of __init__:')
            print('qa_checked: %s'       %  initial_vals['qa_checked'])
            print('qa_approved_by: %s'   %  initial_vals['qa_approved_by'])
            print('qa_approved_date: %s' %  initial_vals['qa_approved_date'])

        # The QA attributes should be passed to the form upon instantiation here:
        super(QANotesForm, self).__init__(*args, **kwargs )
        # The kwarg values are not ending up in the form, though
        kwargs.update(initial=initial_vals)



class BaseExtractedChemicalFormSet(BaseInlineFormSet):
    """
    Base class for the form in which users edit the chemical composition data
    """
    required_css_class = 'required'  # adds to label tag

    class Meta:
        model = ExtractedChemical
        # fields = ['raw_cas', 'raw_chem_name', 'raw_min_comp',
        #           'raw_max_comp', 'unit_type', 'report_funcuse', 'extracted_text']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(BaseExtractedChemicalFormSet, self).__init__(*args, **kwargs)
        for form in self.forms:
            for field in form.fields:
                form.fields[field].widget.attrs.update({'class': 'chem-control'})



@login_required()
def extraction_script_list(request, template_name='qa/extraction_script_list.html'):
    """
    List view of extraction scripts
    """
    # TODO: the user is supposed to be able to click the filter button at the top of the table
    # and toggle between seeing all scripts and seeing only the ones with incomplete QA
    extractionscript = Script.objects.filter(script_type='EX')
    data = {}
    data['object_list'] = extractionscript
    return render(request, template_name, data)


@login_required()
def extraction_script_qa(request, pk,
                         template_name='qa/extraction_script.html'):
    """
    The user reviews the extracted text and checks whether it was properly converted to data
    """
    es = get_object_or_404(Script, pk=pk)
    if es.qa_begun:
        # has qa begun and not complete? if both T, return group to be finished
        if QAGroup.objects.filter(extraction_script=es,
                                  qa_complete=False).exists():
            # return docs that are in extracted texts QA group
            group = QAGroup.objects.get(extraction_script=es,
                                        qa_complete=False)
            texts = ExtractedText.objects.filter(qa_group=group,
                                                 qa_checked=False)
            return render(request, template_name, {'extractionscript': es,
                                                   'extractedtexts': texts,
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
    return render(request, template_name, {'extractionscript': es,
                                           'extractedtexts': texts,
                                           'qagroup': qa_group})


@login_required()
def extraction_script_detail(request, pk,
                             template_name='extraction_script/extraction_script_detail.html'):
    extractionscript = get_object_or_404(Script, pk=pk)
    data = {}
    data['object_list'] = extractionscript
    return render(request, template_name, data)


class ExtractedTextQAForm(ModelForm):
    required_css_class = 'required'  # adds to label tag

    class Meta:
        model = ExtractedText
        fields = ['record_type', 'prod_name', 'data_document', 'qa_checked']



@login_required()
def extracted_text_qa(request, pk, template_name='qa/extracted_text_qa.html', nextid=0):
    """
    Detailed view of an ExtractedText object, where the user can approve the record,
    edit its ExtractedChemical objects, skip to the next ExtractedText in the QA group,
    or exit to the index page
    """
    context = {}
    initial = {}
    extext = get_object_or_404(ExtractedText, pk=pk)
    # The related DataDocument has the same pk as the ExtractedText object
    datadoc = DataDocument.objects.get(pk=pk)
    exscript = extext.extraction_script
    # get the next unapproved Extracted Text object
    # Its ID will populate the URL for the "Skip" button
    if extext.qa_checked:  # if the ExtractedText object's QA process is done, use 0
        nextid = 0
    else:
        nextid = extext.next_extracted_text_in_qa_group()
    # derive the number of approved records and remaining unapproved ones in the QA Group
    a = extext.qa_group.get_approved_doc_count()
    r = ExtractedText.objects.filter(qa_group=extext.qa_group).count() - a
    stats = '%s document(s) approved, %s documents remaining' % (a, r)


    # Create the formset factory for the extracted chemical records
    ChemFormSet = inlineformset_factory(parent_model=ExtractedText,
                                        model=ExtractedChemical,
                                        formset=BaseExtractedChemicalFormSet,
                                        fields=['extracted_text','raw_cas', 'raw_chem_name', 'raw_min_comp',
                                                'raw_max_comp', 'unit_type', 'report_funcuse',
                                                 'ingredient_rank', 'raw_central_comp'],
                                                extra=1)

    if request.method == 'POST' and 'save_no_approval' in request.POST:
        print('--POST')
        print('---saving without approval')

        # Create the form for editing the extracted chemical objects
        chem_formset = ChemFormSet(request.POST, instance=extext, prefix='chemicals')
        # Create the form for editing the extracted text object's QA Notes
        notesform = ExtractedTextForm(request.POST,  instance=extext)
        print('qa_notes in form before is_valid or save() : %s' % notesform['qa_notes'].value())

        print('----VALIDATING FORM AND FORMSET')
        if chem_formset.is_valid():
            print('-----chem_formset validated')
            #saving the changes without approving the ExtractedText object
            if notesform.is_valid():
                print('-------notesform has passed validation')
                notesform.save()

            chem_formset.save()
            extext.qa_edited = True
            extext.save()
            return HttpResponseRedirect(
                        reverse('extracted_text_qa', args=([extext.pk]))
                    )
        else:
            print(chem_formset.errors)

    # APPROVAL
    elif request.method == 'POST' and 'approve' in request.POST:
        print('--POST')
        print('---approving the ExtractedText object')
        nextpk = extext.next_extracted_text_in_qa_group()
        script = extext.extraction_script
        chem_formset = ChemFormSet(request.POST, instance=extext, prefix='chemicals')

        initial = {
            'qa_checked':True,
            'qa_approved_by':request.user,
            'qa_approved_date':datetime.now(),
            'qa_edited':extext.qa_edited,
            }

        notesform = ExtractedTextForm(request.POST, instance=extext, initial=initial )

            # Something is going wrong in the instantiation.
            # The kwargs inside the notesform __init__ method contain what they should ,
            # but by the time the notesform is queried below, it is missing that data
            #   _____
            #  /     \
            # | () () |
            #  \  ^  /
            #   |||||
            #   |||||

        print('--- After initializing notesform, before is_valid()')
        print('qa_checked: %s' % notesform['qa_checked'].data)
        print('qa_approved_by: %s' % notesform['qa_approved_by'].data)
        print('qa_approved_date: %s' % notesform['qa_approved_date'].data)
        print('qa_notes: %s' % notesform['qa_notes'].data)
        #print(notesform)

        if notesform.is_valid():
            print('---- after notesform.is_valid()')
            print('qa_checked: %s' % notesform['qa_checked'].data)
            print('qa_approved_by: %s' % notesform['qa_approved_by'].data)
            print('qa_approved_date: %s' % notesform['qa_approved_date'].data)
            print('qa_notes: %s' % notesform['qa_notes'].data)
            notesform.save()
            print("Script's QA completion status is %s: %s pct of %s " % (script.get_qa_status() , script.get_pct_checked_numeric(), script.get_datadocument_count()))

            if script.get_qa_status():
                print('QA is now complete')
                return HttpResponseRedirect(
                    reverse('extraction_script_qa', args=[(script.pk)])
                )
            else:
                return HttpResponseRedirect(
                    reverse('extracted_text_qa', args=[(nextpk)])
            )
        else:
            print('Trying to approve, but notesform failed validation')
            # re-render the invalid extracted text object's page
            print('Returning the user to the same page for corrections')
            print('----- notesform should be populated with QA attributes:')
            print(notesform)
            # print('----- the POST request:')
            # print(request.POST)
            context = {
                'extracted_text': extext,
                'doc': datadoc,
                'script': exscript,
                'stats': stats,
                'nextid': nextid,
                'chem_formset': chem_formset,
                'notesform': notesform,
            }
            return render(request, template_name,context)

    else:
        # GET request
        print('GET request')
        notesform =  ExtractedTextForm(instance=extext)
        chem_formset = ChemFormSet(instance=extext, prefix='chemicals')
        context = {
            'extracted_text': extext,
            'doc': datadoc,
            'script': exscript,
            'stats': stats,
            'nextid': nextid,
            'chem_formset': chem_formset,
            'notesform': notesform,
        }
        #print(context)
        return render(request, template_name, context)
