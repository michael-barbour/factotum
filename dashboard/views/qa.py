import django_filters

from django.shortcuts import render
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


""" class ExtractedChemicalsEditView(XEditableDatatableView):
    model = ExtractedChemical
    datatable_options = {
        'columns': [
            'id',
            ("CAS", 'raw_cas', helpers.make_xeditable),
            ("Chemical Name", 'raw_chem_name', helpers.make_xeditable),
            ("Minimum Composition", 'raw_min_comp', helpers.make_xeditable),
            ("Maximum Composition", 'raw_max_comp', helpers.make_xeditable),
            ("Units", 'units', helpers.make_xeditable),
            ("Reported Functional Use", "report_funcuse", helpers.make_xeditable),
        ]
    } """