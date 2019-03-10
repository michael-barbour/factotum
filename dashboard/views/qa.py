from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q

from dashboard.models import Script


@login_required()
def qa_extractionscript_index(request, template_name='qa/extraction_script_index.html'):
    datadocument_count = Count('extractedtext__extraction_script')
    qa_complete_extractedtext_count = Count('extractedtext', filter=Q(extractedtext__qa_checked=True))
    extraction_scripts = Script.objects.\
        annotate(datadocument_count=datadocument_count).\
        annotate(qa_complete_extractedtext_count=qa_complete_extractedtext_count).\
        filter(script_type='EX')
    return render(request, template_name, {'extraction_scripts': extraction_scripts})
