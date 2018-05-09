import math
from random import shuffle
import os
from datetime import datetime
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.forms import ModelForm, Form, BaseInlineFormSet, inlineformset_factory, TextInput, CharField

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


class ExtractedChemicalForm(Form):
    """
    Form for individual extracted chemical entries
    """
    raw_cas = CharField(
        max_length=50,
        widget=TextInput(attrs={
            'placeholder': 'CAS Number',
        }),
        required=False)
    raw_chem_name = CharField(
        max_length=500,
        widget=TextInput(attrs={
            'placeholder': 'Chemical Name',
        }),
        required=False)


class BaseExtractedChemicalFormSet(BaseInlineFormSet):
    required_css_class = 'required'  # adds to label tag

    class Meta:
        model = ExtractedChemical
        fields = ['raw_cas', 'raw_chem_name', 'raw_min_comp',
                  'raw_max_comp', 'unit_type', 'report_funcuse', ]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(BaseExtractedChemicalFormSet, self).__init__(*args, **kwargs)


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
            texts = ExtractedText.objects.filter(qa_group=group,
                                                 qa_checked=False)
            return render(request, template_name, {'extractionscript': es,
                                                   'extractedtexts': texts,
                                                   'qagroup': group})
    # pks of text and docs are the same!
    doc_text_ids = ExtractedText.objects.filter(extraction_script=pk)
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
    extracted = get_object_or_404(ExtractedText, pk=pk)
    nextpk = extracted.next_extracted_text_in_qa_group()
    extracted.qa_checked = True
    extracted.qa_status = ExtractedText.APPROVED_WITHOUT_ERROR
    extracted.qa_approved_date = datetime.now()
    extracted.qa_approved_by = request.user
    extracted.save()
    return HttpResponseRedirect(
        reverse('extracted_text_qa', args=([nextpk]))
    )


@login_required()
def extracted_text_qa(request, pk, template_name='qa/extracted_text_qa.html', nextid=0):

    extext = get_object_or_404(ExtractedText, pk=pk)
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

    # Create the formset
    ChemFormSet = inlineformset_factory(ExtractedText, ExtractedChemical,
                                        formset=BaseExtractedChemicalFormSet,
                                        fields=['raw_cas', 'raw_chem_name', 'raw_min_comp',
                                                'raw_max_comp', 'unit_type', 'report_funcuse',
                                                'weight_fraction_type', 'ingredient_rank', 'raw_central_comp'])
    user = request.user
    et = ExtractedText.objects.get(pk=pk)

    # The initial data are the extracted chemicals related to the extracted text
    text_chems = ExtractedChemical.objects.filter(
        extracted_text=et).order_by('ingredient_rank')
    chem_data = [{'raw_cas': chem.raw_cas,
                  'raw_chem_name': chem.raw_chem_name,
                  'raw_min_comp': chem.raw_min_comp,
                  'raw_max_comp': chem.raw_max_comp,
                  'unit_type': chem.unit_type,
                  'report_funcuse': chem.report_funcuse,
                  'weight_fraction_type': chem.weight_fraction_type,
                  'ingredient_rank': chem.ingredient_rank,
                  'raw_central_comp': chem.raw_central_comp,
                  }
                 for chem in text_chems]

    if request.method == 'POST':
        #text_form = ExtractedTextForm(request.POST, user=user)
        print('POST request, creating chem_formset from ChemFormset()')
        chem_formset = ChemFormSet(initial=request.POST)
        if chem_formset.is_valid():
            print('chem_formset validated')
            chem_formset.save()
            # Now save the data for each form in the formset
            new_chems = []

            for chem_form in chem_formset:
                raw_cas = chem_form.cleaned_data.get('raw_cas')
                raw_chem_name = chem_form.cleaned_data.get('raw_chem_name')
                raw_min_comp = chem_form.cleaned_data.get('raw_min_comp')
                raw_max_comp = chem_form.cleaned_data.get('raw_max_comp')
                unit_type = chem_form.cleaned_data.get('unit_type')
                report_funcuse = chem_form.cleaned_data.get('report_funcuse')
                weight_fraction_type = chem_form.cleaned_data.get(
                    'weight_fraction_type')
                ingredient_rank = chem_form.cleaned_data.get('ingredient_rank')
                raw_central_comp = chem_form.cleaned_data.get(
                    'raw_central_comp')
                chem_form.save()

                if raw_cas and raw_chem_name:
                    new_chems.append(ExtractedChemical(
                        extracted_text=et, raw_cas=raw_cas, raw_chem_name=raw_chem_name))

            try:
                with transaction.atomic():
                    # Replace the old with the new
                    ExtractedChemical.objects.filter(
                        extracted_text=et).delete()
                    ExtractedChemical.objects.bulk_create(new_chems)

                    # And notify our users that it worked
                    messages.success(
                        request, 'You have updated the chemicals.')

            except IntegrityError:  # If the transaction failed
                messages.error(
                    request, 'There was an error saving the extracted chemicals.')
                # return redirect(reverse('profile-settings'))

    else:
        # GET request
        data={        
            'chemicals-TOTAL_FORMS': '1',
            'chemicals-INITIAL_FORMS': '0',
            'chemicals-MAX_NUM_FORMS': ''
            }
        chem_formset = ChemFormSet(initial=chem_data)

    context = {
        'extracted': extext,
        'doc': datadoc, 
        'script': exscript, 
        'chem_formset': chem_formset, 
        'stats': stats, 
        'nextid': nextid,
        'chem_formset': chem_formset,
    }

    return render(request, template_name, context)


@login_required()
def extracted_chemical_update(request, pk):
    exchem = get_object_or_404(ExtractedChemical, pk=pk)
    form = ExtractedChemicalForm(request.POST or None, instance=exchem)
    if form.is_valid():
        form.save()
        return redirect('extracted_text_qa', exchem.extracted_text.pk)
    return render(request, 'data_group/datagroup_form.html', {'form': form})
