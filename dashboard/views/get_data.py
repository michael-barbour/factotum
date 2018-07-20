
from django.shortcuts import render
from django.http import HttpResponse
import datetime
import csv
from dashboard.models import DSSToxSubstance, DataDocument, PUC, Product, ExtractedChemical
from django.db.models import Count, Q


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

    dds_wf_n = DSSToxSubstance.objects.filter(sid__in=dtxs).distinct().\
        filter(Q(extracted_chemical__raw_central_comp__isnull=False) | Q(extracted_chemical__raw_min_comp__isnull=False) | Q(extracted_chemical__raw_central_comp__isnull=False)).annotate(dds_wf_n=Count('ingredient__product__datadocument')).values('sid','true_chemname', 'dds_wf_n')
    stats.append(dds_wf_n)

    products_n = DSSToxSubstance.objects.filter(sid__in=dtxs).distinct().\
        annotate(products_n=Count('ingredient__product')).values('sid','true_chemname', 'products_n')
    stats.append(products_n)

    return stats



def download_chem_stats():
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="chem_summary_metrics_%s.csv"' % (datetime.datetime.now().strftime("%Y%m%d"))

    writer = csv.writer(response)
    writer.writerow(['DTXSID', 'true_chemname', 'pucs_n', 'dds_n', 'dds_wf_n', 'products_n'])

    return response