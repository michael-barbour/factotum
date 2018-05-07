import django_filters
from django.forms import ModelForm, Form
from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth.decorators import login_required

from dashboard.models import Script, ExtractedText, DataDocument, QAGroup, ExtractedChemical

# we are not currently using this class


class ExtractionScriptFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = Script
        fields = ['url']


@login_required()
def qa_index(request, template_name='qa/qa_index.html'):

    scripts = Script.objects.filter(script_type='EX')
    return render(request, template_name, {'extraction_scripts': scripts})


@login_required()
def extracted_chemical_update(request, pk):
    exchem = get_object_or_404(ExtractedChemical, pk=pk)
    form = ExtractedChemicalForm(request.POST or None, instance=exchem)
    if form.is_valid():
        form.save()
        return redirect('extracted_text_qa', exchem.extracted_text.pk)
    return render(request, 'data_group/datagroup_form.html', {'form': form})


class ExtractedChemicalForm(ModelForm):
    required_css_class = 'required' # adds to label tag

    class Meta:
        model = ExtractedChemical
        fields = ['raw_cas', 'raw_chem_name', 'raw_min_comp', 'raw_max_comp', 'unit_type', 'report_funcuse',]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(ExtractedChemicalForm, self).__init__(*args, **kwargs)
