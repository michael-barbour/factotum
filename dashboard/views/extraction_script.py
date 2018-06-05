import math
from random import shuffle
import os
from datetime import datetime
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.forms import ModelForm, Form, BaseInlineFormSet, inlineformset_factory, TextInput, CharField, Textarea

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

class QANotesForm(ModelForm):

    class Meta:
        model = ExtractedText
        fields = ['qa_notes']
        labels = {
            'qa_notes': _('QA Notes (required after recording any changes to extracted chemicals)'),
        }
    def clean_qa_notes(self):
        data = self.cleaned_data['qa_notes']
        if data is None and self.cleaned_data['qa_status'] == ExtractedText.APPROVED_WITH_ERROR :
            raise forms.ValidationError("The extracted text needs QA notes")
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(QANotesForm, self).__init__(*args, **kwargs)
        self.fields['qa_notes'].widget.attrs.update({'class': 'chem-control form-inline', 'size': '80'})

class BaseExtractedChemicalFormSet(BaseInlineFormSet):
    """
    Base class for the form in which users edit the chemical composition data
    """
    required_css_class = 'required'  # adds to label tag

    class Meta:
        model = ExtractedChemical
        fields = ['raw_cas', 'raw_chem_name', 'raw_min_comp',
                  'raw_max_comp', 'unit_type', 'report_funcuse', 'extracted_text']

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
def extracted_text_approve(request, pk):
    """
    This view is posted when the user approves an ExtractedText object without changes.
    Check if the approval puts the Script object across the QA Complete line
    """
    extracted = get_object_or_404(ExtractedText, pk=pk)
    print('\nExtractedText object: %s' % extracted)
    nextpk = extracted.next_extracted_text_in_qa_group()
    extracted.qa_checked = True
    extracted.qa_status = ExtractedText.APPROVED_WITHOUT_ERROR
    extracted.qa_approved_date = datetime.now()
    extracted.qa_approved_by = request.user
    
    script = extracted.extraction_script
    # What share of the Script's ExtractedText objects have been approved before the save?
    pct_before = script.get_pct_checked()
    extracted.save()
    pct_after = script.get_pct_checked()
    print("Percent checked before approval: %s \nAfter approval: %s" % (pct_before, pct_after))
    print("Script's QA completion status: %s " % script.get_qa_status() )
    if script.get_qa_status():
        return HttpResponseRedirect(
            reverse('extraction_script_qa', args=([script.pk]))
        )
    else:
        return HttpResponseRedirect(
            reverse('extracted_text_qa', args=([nextpk]))
        )



@login_required()
def extracted_text_qa(request, pk, template_name='qa/extracted_text_qa.html', nextid=0):
    """
    Detailed view of an ExtractedText object, where the user can approve, edit, skip, or exit
    """
    extext = get_object_or_404(ExtractedText, pk=pk)
    # The related DataDocument has the same pk as the ExtractedText object
    datadoc = DataDocument.objects.get(pk=pk)
    exscript = extext.extraction_script
    # get the next unapproved Extracted Text object
    # Its ID will populate the URL for the "Skip" button
    if extext.qa_checked:
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
                                                'weight_fraction_type', 'ingredient_rank', 'raw_central_comp'],
                                                extra=1)
    user = request.user
    if request.method == 'POST':
        print('------POST---------')
        # print(request.POST)
        # Create the form for editing the extracted text object's QA Notes
        notesform = QANotesForm(request.POST,  instance=extext)
        # Create the form for editing the extracted chemical objects
        chem_formset = ChemFormSet(request.POST, instance=extext, prefix='chemicals')
        print('------VALIDATING FORM AND FORMSET------')

        if chem_formset.is_valid():
            print('chem_formset validated')
            script = extext.extraction_script
            if 'save_with_approval' in request.POST :
                # if the user was approving the extracted text with the edits, follow the
                # appropriate path
                print('------saving changes to chemicals, approving ExtractedText object------')
                if notesform.is_valid():
                    print('the notes form for the ExtractedText object is valid')
                    print('Contents of notesform.cleaned_data["qa_notes"]: %s' % notesform.cleaned_data['qa_notes'])
                    extext.qa_checked = True
                    extext.qa_status = ExtractedText.APPROVED_WITH_ERROR
                    extext.qa_approved_date = datetime.now()
                    extext.qa_approved_by = request.user
                    extext.qa_notes = notesform['qa_notes'].value()
                    extext.save()
                print('ExtractedText object: %s' % extext)
                chem_formset.save()

                print("Script's QA completion status: %s " % script.get_qa_status() )
                print(script.get_pct_checked_numeric())
                if script.get_qa_status():
                    return HttpResponseRedirect(
                        reverse('extraction_script_qa', args=([script.pk]))
                    )
                else:
                    return HttpResponseRedirect(
                        reverse('extracted_text_qa', args=([nextid]))
                    )
            else:
                #saving the changes without approving the ExtractedText object
                print('qa_notes in form before save() : %s' % notesform['qa_notes'].value())
                notesform.save()
                chem_formset.save()
                
                if notesform.is_valid():
                    print('the notes form for the ExtractedText object is valid')
                    print('Contents of notesform.cleaned_data["qa_notes"]: %s' % notesform.cleaned_data['qa_notes'])
                print('ExtractedText object qa_notes after save() : %s' % extext.qa_notes)

        else:
            print(chem_formset.errors)
    else:
        # GET request
        notesform =  QANotesForm(instance=extext)
        chem_formset = ChemFormSet(instance=extext, prefix='chemicals')

    context = {
        'extracted_text': extext,
        'doc': datadoc, 
        'script': exscript, 
        'chem_formset': chem_formset, 
        'stats': stats, 
        'nextid': nextid,
        'chem_formset': chem_formset,
        'notesform': notesform,
    }
    #print(context)
    return render(request, template_name, context)

