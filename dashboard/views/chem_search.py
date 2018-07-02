from django.http import JsonResponse
from dashboard.models import DataDocument
from django.db.models import Q


def chem_search(request):

    chemical = request.GET['chemical']
    dd_all = DataDocument.objects.filter(Q(extractedtext__extractedchemical__raw_chem_name__icontains=chemical) |
                                              Q(extractedtext__extractedchemical__raw_cas__icontains=chemical))

    dd_match = DataDocument.objects.filter(Q(extractedtext__extractedchemical__dsstoxsubstance__true_chemname__icontains=chemical) |
                                           Q(extractedtext__extractedchemical__dsstoxsubstance__true_cas__icontains=chemical))

    # dd_probable = dd_all.difference(dd_match) # Not supported by MySQL!!!

    dd_probable = DataDocument.objects.filter(Q(extractedtext__extractedchemical__raw_chem_name__icontains=chemical) |
                                              Q(extractedtext__extractedchemical__raw_cas__icontains=chemical)
                                              ).exclude(id__in=dd_match)

    count_dd_probable = dd_probable.count()
    count_dd_match = dd_match.count()

    columns = ['title', 'data_group_id', 'document_type_id']
    matched_objects = []
    for i in dd_match.values():
        ret = [i[j] for j in columns]
        matched_objects.append(ret)

    probable_objects = []
    for i in dd_probable.values():
        ret = [i[j] for j in columns]
        probable_objects.append(ret)


    return JsonResponse({
        "Matched Data Documents": count_dd_match,
        "Probable Data Document matches": count_dd_probable,
        "Matched Records": matched_objects,
        "Probable Records": probable_objects,
    })
