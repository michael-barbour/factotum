from dal import autocomplete

from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.decorators import login_required

from dashboard.models import *
from dashboard.forms import ExtractedTextForm, HabitsPUCForm, HnPFormSet


@login_required()
def habitsandpractices(request, pk,
                      template_name='data_group/habitsandpractices.html'):
    doc = get_object_or_404(DataDocument, pk=pk, )
    script = Script.objects.last() # this needs to be changed bewfore checking in!
    extext, created = ExtractedText.objects.get_or_create(data_document=doc,
                                                    extraction_script=script)
    if created:
        extext.doc_date = 'please add...'
    # print(extext.pk)
    ext_form = ExtractedTextForm(request.POST or None, instance=extext)
    hp_formset = HnPFormSet(request.POST or None, instance=extext, prefix='habits')
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
    form = HabitsPUCForm()
    if request.method == 'POST':
        form = HabitsPUCForm(request.POST)
        if form.is_valid():
            print(form['puc'].value())
            puc = PUC.objects.get(id=form['puc'].value())
            # make sure the PUC link doesn't already exist
            if not ExtractedHabitsAndPracticesToPUC.objects.filter(
                    PUC=puc,
                    extracted_habits_and_practices=hnp).exists():
                ExtractedHabitsAndPracticesToPUC.objects.create(
                        PUC=puc,
                        extracted_habits_and_practices=hnp
                )
                form = HabitsPUCForm()
    linked = ExtractedHabitsAndPracticesToPUC.objects.filter(
                    extracted_habits_and_practices=hnp
    ).values('PUC')
    hnp_puc = PUC.objects.filter(pk__in=linked)
    print(hnp_puc)
    context = {'hnp': hnp,
                'form': form,
                'hnp_puc': hnp_puc,
    }
    return render(request, template_name, context)
