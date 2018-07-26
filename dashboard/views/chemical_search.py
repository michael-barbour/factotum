from django.http import JsonResponse
from django.shortcuts import render
from dashboard.models import DataDocument, ExtractedChemical, DSSToxSubstance
from django.db.models import Q
from haystack.query import SearchQuerySet

def chem_search(request, template_name='search/chemical_search.html'):
    return render(request,
                  template_name,
                  {'results': chem_search_results(request.GET['q'])})

def chem_search_json_view(request):
    results = chem_search_results(request.GET['chemical'])
    results['matchedRecords'] = list(
        results['matchedRecords'].values('title', 'id', 'data_group_id', 'document_type_id'))
    results['probableRecords'] = list(
        results['probableRecords'].values('title', 'id', 'data_group_id', 'document_type_id'))
    return JsonResponse(results)

def chem_search_results(chemical):
    # Get matching DSSToxSubstance records
    sqs_dsstox = SearchQuerySet().filter(content=chemical).models(DSSToxSubstance)
    dsstox_doc_ids = list()

    # Get a list of the Data Document IDs for the results
    for dsstox in sqs_dsstox:
        dsstox_doc_ids.append(dsstox.data_document_id)

    # Get matching Extracted Chemical records
    sqs_exchem = SearchQuerySet().filter(content=chemical).models(ExtractedChemical)
    exchem_doc_ids = list()

    # Get a list of the Data Document IDs for the results
    for exchem in sqs_exchem:
        exchem_doc_ids.append(exchem.object.extracted_text.data_document.id)

    # Retrieve DataDocuments that match theses two sets themselves, so we have access to their other attributes
    dd_match = DataDocument.objects.filter(id__in=dsstox_doc_ids)
    dd_probable = DataDocument.objects.filter(Q(id__in=exchem_doc_ids) & ~Q(id__in=dsstox_doc_ids))

    # Counts of each result set
    count_dd_probable = dd_probable.count()
    count_dd_match = dd_match.count()

    return {
        "queryString": chemical,
        "matchedDataDocuments": count_dd_match,
        "probableDataDocumentMatches": count_dd_probable,
        "matchedRecords": dd_match,
        "probableRecords": dd_probable,
    }
