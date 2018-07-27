from dal import autocomplete

from django import forms
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from dashboard.models import *


class ExtractedTextForm(forms.ModelForm):

    class Meta:
        model = ExtractedText
        fields = ['doc_date', 'data_document', 'extraction_script']
        widgets = {
            'data_document': forms.HiddenInput(),
            'extraction_script': forms.HiddenInput(),
        }

class HabitsPUCForm(forms.ModelForm):
    puc = forms.ModelChoiceField(
        queryset=PUC.objects.all(),
        label='PUC',
        widget=autocomplete.ModelSelect2(
            url='habit-autocomplete',
            attrs={'data-minimum-input-length': 3,  })
    )

    class Meta:
        model = ExtractedHabitsAndPracticesToPUC
        fields = ['puc']

@login_required()
def habitsandpractices(request, pk,
                      template_name='data_group/habitsandpractices.html'):
    doc = get_object_or_404(DataDocument, pk=pk, )
    script = Script.objects.last() # this needs to be changed bewfore checking in!
    extext, created = ExtractedText.objects.get_or_create(data_document=doc,
                                                    extraction_script=script)
    if created:
        extext.doc_date = 'please add...'
    HPFormSet = forms.inlineformset_factory(parent_model=ExtractedText,
                                        model=ExtractedHabitsAndPractices,
                                        fields=['product_surveyed','mass',
                                                'mass_unit', 'frequency',
                                                'frequency_unit',
                                                'duration', 'duration_unit',
                                                'prevalence', 'notes'],
                                                extra=1)
    # print(extext.pk)
    ext_form = ExtractedTextForm(request.POST or None, instance=extext)
    hp_formset = HPFormSet(request.POST or None, instance=extext, prefix='habits')
    context = {   'doc'         : doc,
                  'ext_form'    : ext_form,
                  'hp_formset'  : hp_formset,
                  }
    if request.method == 'POST' and 'save' in request.POST:
        # HPFormSet()
        print(hp_formset.is_valid())
        # print(ext_form.cleaned_data['data_document'])
        # print(ext_form.cleaned_data['extraction_script'])
        # print(ext_form.cleaned_data['doc_date'])
        # print(ext_form.non_field_errors())
        if hp_formset.is_valid():
            hp_formset.save()
        if ext_form.is_valid():
            ext_form.save()
        doc.extracted = True
        doc.save()
        context = {   'doc'         : doc,
                      'ext_form'    : ext_form,
                      'hp_formset'  : hp_formset,
                      }
        # render(request, template_name, context)
        # return redirect('habitsandpractices', pk=doc.id)
    return render(request, template_name, context)


@login_required()
def link_habitsandpractices(request, pk,
                      template_name='data_group/habitsandpractices_to_puc.html'):
    hnp = get_object_or_404(ExtractedHabitsAndPractices, pk=pk, )
    form = HabitsPUCForm(request.POST or None)
    context = {'hnp': hnp,
                'form': form,
    }
    return render(request, template_name, context)
