
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from dashboard.models import Script, ExtractedText, DataDocument, QAGroup


@login_required()
def qa_index(request, template_name='qa/qa_index.html'):

    scripts = Script.objects.filter(script_type='EX')
    return render(request, template_name, {'extraction_scripts': scripts})



