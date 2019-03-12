from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q

from dashboard.models import Script, DataGroup, DataDocument, ExtractedCPCat


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
    datagroup = get_object_or_404(DataGroup, pk=pk, group_type__code='CP')
    datadocuments = DataDocument.objects.filter(data_group=datagroup)
    for datadocument in datadocuments:
        datadocument.prep_for_cp_qa()
    return render(request, template_name, {'datagroup':datagroup, 'datadocuments':datadocuments})

@login_required()
def extracted_cpccat_qa(request, pk,
                            template_name='qa/extracted_cpccat_qa.html', nextid=0):
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

    ParentForm, ChildForm = create_detail_formset(doc, EXTRA)
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
        # print(request.__dict__)

        ParentForm, ChildForm = create_detail_formset(doc, EXTRA)
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
                print(detail_formset.errors)
                # TODO: iterate through this dict of errors and map each error to
                # the corresponding form in the template for rendering

            context['detail_formset'] = detail_formset
            context['ext_form'] = ext_form
            context.update({'notesform': notesform})  # calls the clean method? y?

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
                    reverse('qa_extractionscript'))
    return render(request, template_name, context)

