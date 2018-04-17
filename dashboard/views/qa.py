import django_filters

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from dashboard.models import Script, ExtractedText, DataDocument, QAGroup

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



