from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from dashboard.views import *
from dashboard.models import DataSource, DataDocument, ExtractionScript
import django_filters

class ExtractionScriptFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = ExtractionScript
        fields = ['url']

@login_required()
def qa_index(request, template_name='qa/qa_index.html'):

    extractionscripts = ExtractionScript.objects.all()
    return render(request, template_name, {'extraction_scripts': extractionscripts})
