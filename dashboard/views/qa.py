from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from dashboard.views import *
from dashboard.models import DataSource, DataDocument, ExtractionScript

@login_required()
def qa_index(request, template_name='qa/qa_index.html'):

    extraction_scripts = ExtractionScript.objects.distinct()
    return render(request, template_name, {'qa': extraction_scripts})