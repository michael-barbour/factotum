from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import ValidationError, MultipleObjectsReturned, ObjectDoesNotExist
from django.urls import reverse
from django.utils import timezone

from dashboard.forms import create_detail_formset, QANotesForm
from dashboard.models import Script, DataGroup, DataDocument, ExtractedCPCat, ExtractedText, QAGroup, QANotes
from factotum.settings import EXTRA


@login_required()
def qa_extractionscript_index(request, template_name='qa/extraction_script_index.html'):
    datadocument_count = Count('extractedtext__extraction_script')
    qa_complete_extractedtext_count = Count('extractedtext', filter=Q(extractedtext__qa_checked=True))
    extraction_scripts = Script.objects.\
        annotate(datadocument_count=datadocument_count).\
        annotate(qa_complete_extractedtext_count=qa_complete_extractedtext_count).\
        filter(script_type='EX')

    return render(request, template_name, {'extraction_scripts': extraction_scripts})

@login_required()
def qa_chemicalpresence_index(request, template_name='qa/chemical_presence_index.html'):
    datagroups = DataGroup.objects.filter(group_type__code='CP').\
        annotate(datadocument_count=Count('datadocument'))

    return render(request, template_name, {'datagroups': datagroups})

@login_required()
def qa_chemicalpresence(request, pk, template_name='qa/chemical_presence.html'):
    datagroup = DataGroup.objects.get(pk=pk)
    if datagroup.group_type.code != 'CP':
        raise ValidationError('This DataGroup is not of a ChemicalPresence type')
    extractedcpcats = ExtractedCPCat.objects.filter(data_document__data_group=datagroup)
    for extractedcpcat in extractedcpcats:
        print(extractedcpcat.data_document)
        extractedcpcat.prep_for_cp_qa()
    return render(request, template_name, {'datagroup':datagroup, 'extractedcpcats':extractedcpcats})

@login_required()
def qa_extraction_script(request, pk,
                         template_name='qa/extraction_script.html'):
    """
    The user reviews the extracted text and checks whether it was properly converted to data
    """
    es = get_object_or_404(Script, pk=pk)
    # If the Script has no related ExtractedText objects, redirect back to the QA index
    if ExtractedText.objects.filter(extraction_script = es).count() == 0 :
        return redirect('/qa/extractionscript/')
    # Check whether QA has begun for the script
    if es.qa_begun:
        # if the QA process has begun, there should already be one QA Group
        # associated with the Script.
        try:
            # get the QA Group
            qa_group = QAGroup.objects.get(extraction_script=es,
                                           qa_complete=False)
        except MultipleObjectsReturned:
            qa_group = QAGroup.objects.filter(extraction_script=es,
                                              qa_complete=False).first()
        except ObjectDoesNotExist:
            print('No QA Group was found matching Extraction Script %s' % es.pk)

        texts = ExtractedText.objects.filter(qa_group=qa_group,
                                             qa_checked=False)
        return render(request, template_name, {'extractionscript': es,
                                               'extractedtexts': texts,
                                               'qagroup': qa_group})
    else:
        qa_group = es.create_qa_group()
        es.qa_begun = True
        es.save()
    # Collect all the ExtractedText objects in the QA Group
    texts = ExtractedText.objects.filter(qa_group=qa_group)

    return render(request, template_name, {'extractionscript': es,
                                           'extractedtexts': texts,
                                           'qagroup': qa_group})


@login_required()
def extracted_text_qa(request, pk,
                      template_name='qa/extracted_text_qa.html', nextid=0):
    """
    Detailed view of an ExtractedText object, where the user can approve the
    record, edit its ExtractedChemical objects, skip to the next ExtractedText
    in the QA group, or exit to the index page
    """
    extext = get_object_or_404(ExtractedText, pk=pk)
    # The related DataDocument has the same pk as the ExtractedText object
    doc = DataDocument.objects.get(pk=pk)
    exscript = extext.extraction_script
    # when not coming from extraction_script page, we don't necessarily have a qa_group created
    if not extext.qa_group:
        # create the qa group with the optional ExtractedText pk argument
        # so that the ExtractedText gets added to the QA group even if the
        # group uses a random sample
        qa_group = exscript.create_qa_group(pk)
        exscript.qa_begun = True
        exscript.save()
        extext.qa_group = qa_group
        extext.save()
    # get the next unapproved Extracted Text object
    # Its ID will populate the URL for the "Skip" button
    if extext.qa_checked:  # if ExtractedText object's QA process done, use 0
        nextid = 0
    else:
        nextid = extext.next_extracted_text_in_qa_group()
    # derive number of approved records and remaining unapproved in QA Group

    a = extext.qa_group.get_approved_doc_count()
    r = ExtractedText.objects.filter(qa_group=extext.qa_group).count() - a
    stats = '%s document(s) approved, %s documents remaining' % (a, r)
    referer = 'data_document' if 'datadocument' in request.path else 'qa_extraction_script'

    # Create the formset factory for the extracted records
    # The model used for the formset depends on whether the
    # extracted text object matches a data document()
    # The QA view should exclude the weight_fraction_type field.
    ParentForm, ChildForm = create_detail_formset(
        doc, EXTRA, can_delete=True, exclude=['weight_fraction_type'])
    # extext = extext.pull_out_cp()
    ext_form = ParentForm(instance=extext)
    detail_formset = ChildForm(instance=extext)
    # Add CSS selector classes to each form
    for form in detail_formset:
        for field in form.fields:
            form.fields[field].widget.attrs.update(
                {'class': f'detail-control form-control %s' % doc.data_group.type}
            )

    note, created = QANotes.objects.get_or_create(extracted_text=extext)
    notesform = QANotesForm(instance=note)

    context = {
        'extracted_text': extext,
        'doc': doc,
        'script': exscript,
        'stats': stats,
        'nextid': nextid,
        'detail_formset': detail_formset,
        'notesform': notesform,
        'ext_form': ext_form,
        'referer': referer
    }

    if request.method == 'POST' and 'save' in request.POST:

        ParentForm, ChildForm = create_detail_formset(
            doc, EXTRA, can_delete=True, exclude=['weight_fraction_type'])
        # extext = extext.pull_out_cp()
        ext_form = ParentForm(request.POST, instance=extext)
        detail_formset = ChildForm(request.POST, instance=extext)

        notesform = QANotesForm(request.POST, instance=note)
        notesform.save()
        if detail_formset.has_changed() or ext_form.has_changed():
            if detail_formset.is_valid() and ext_form.is_valid():
                detail_formset.save()
                ext_form.save()
                extext.qa_edited = True
                extext.save()
                # rebuild the formset after saving it
                detail_formset = ChildForm(instance=extext)
            else:
                pass
                # print(detail_formset.errors)
                # TODO: iterate through this dict of errors and map each error to
                # the corresponding form in the template for rendering

            context['detail_formset'] = detail_formset
            context['ext_form'] = ext_form
            # calls the clean method? y?
            context.update({'notesform': notesform})

        # Add CSS selector classes to each form
        for form in detail_formset:
            for field in form.fields:
                form.fields[field].widget.attrs.update(
                    {'class': f'detail-control form-control %s' % doc.data_group.type}
                )

    elif request.method == 'POST' and 'approve' in request.POST:  # APPROVAL
        notesform = QANotesForm(request.POST, instance=note)
        context['notesform'] = notesform
        nextpk = extext.next_extracted_text_in_qa_group()
        if notesform.is_valid():
            extext.qa_approved_date = timezone.now()
            extext.qa_approved_by = request.user
            extext.qa_checked = True
            extext.save()
            notesform.save()
            if referer == 'data_document':
                return HttpResponseRedirect(
                    reverse(referer, kwargs={'pk': pk}))
            elif not nextpk == 0:
                return HttpResponseRedirect(
                    reverse('extracted_text_qa', args=[(nextpk)]))
            elif nextpk == 0:
                return HttpResponseRedirect(
                            reverse('qa_extractionscript_index'))
    return render(request, template_name, context)
