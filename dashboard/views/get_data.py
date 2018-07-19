
from django.shortcuts import render
from django.http import HttpResponse
import csv
from dashboard.models import DSSToxSubstance, DataDocument, PUC, Product, ExtractedChemical
from django.db.models import Count


def get_data(request, template_name='get_data/get_data.html'):

    return render(request, template_name)

def stats_by_dtxsids(dtxs):
    """     
    PUCS.n
    The number of unique PUCs (product categories) the chemical is associated with

    datadocs.n
    "The number of data documents (e.g.  MSDS, SDS, ingredient list, product label) the chemical is appears in"

    datadocs_w_wf.n
    "The number of data documents with associated weight fraction data that the chemical appears in (weight fraction data may be reported or predicted data, i.e., predicted from an ingredient list)"

    products.n
    "The number of products the chemical appears in, where a product is defined as a product entry in Factotum." 
    """
    print(dtxs)
    stats = []
    pucs_n = DSSToxSubstance.objects.filter(sid__in=dtxs).distinct().\
        annotate(pucs_n=Count('ingredient__product__puc')).values('sid','true_chemname', 'pucs_n')
    stats.append(pucs_n)

    dds_n = DSSToxSubstance.objects.filter(sid__in=dtxs).distinct().\
        annotate(dds_n=Count('ingredient__product__datadocument')).values('sid','true_chemname', 'dds_n')
    stats.append(dds_n)
    return stats



def download_chem_stats(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="s.csv"'

    writer = csv.writer(response)
    writer.writerow(['gen_cat', 'prod_fam', 'prod_type', 'description', 'PUC_type'])
    for puc in PUC.objects.all():
        attr = puc.attribute if puc.attribute != None else ''
        writer.writerow([puc.gen_cat, puc.prod_fam, puc.prod_type,
                                                        puc.description, attr])

    return response