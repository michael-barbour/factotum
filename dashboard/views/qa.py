from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.http import HttpResponse

from dashboard.models import Script, DataGroup, DataDocument


@login_required()
def qa_extractionscript_index(request, template_name='qa/extraction_script_index.html'):
    datadocument_count = Count('extractedtext__extraction_script')
    qa_complete_extractedtext_count = Count('extractedtext', filter=Q(extractedtext__qa_checked=True))
    extraction_scripts = Script.objects.\
        annotate(datadocument_count=datadocument_count).\
        annotate(qa_complete_extractedtext_count=qa_complete_extractedtext_count).\
        filter(script_type='EX')

    return render(request, template_name, {'extraction_scripts': extraction_scripts})

def qa_chemicalpresence_index(request, template_name='qa/chemical_presence_index.html'):
    datagroups = DataGroup.objects.filter(group_type__code='CP').\
        annotate(datadocument_count=Count('datadocument'))

    return render(request, template_name, {'datagroups': datagroups})

def qa_chemicalpresence(request, pk, template_name='qa/chemical_presence.html'):
    datagroup = get_object_or_404(DataGroup, pk=pk, group_type__code='CP')
    datadocuments = DataDocument.objects.filter(data_group=datagroup)
    print(datadocuments.query)

    return render(request, template_name, {'datagroup':datagroup, 'datadocuments':datadocuments})

@login_required()
def chemical_presence_qa(request, pk,
                            template_name='qa/chemical_presence_qa.html', nextid=0):
    return render(request, template_name)


@login_required()
def flag_qa_children(request, pk ):
    doc = get_object_or_404(DataDocument, pk=pk)
    return HttpResponse(f"{doc}, we have a problem.")