
from django.shortcuts import render
from django.http import HttpResponse
import datetime
import csv
from dashboard.models import DSSToxSubstance, DataDocument, PUC, Product, ExtractedChemical, ExtractedText
from django.db.models import Count, Q, Value, IntegerField, Subquery, OuterRef
from django.forms.models import model_to_dict



def get_data(request, template_name='get_data/get_data.html'):

    return render(request, template_name)

def stats_by_dtxsids(dtxs):
    """     
    PUCS.n
    The number of unique PUCs (product categories) the chemical is associated with

    datadocs.n
    "The number of data documents (e.g.  MSDS, SDS, ingredient list, product label) 
    the chemical is appears in"

    datadocs_w_wf.n
    "The number of data documents with associated weight fraction data 
    that the chemical appears in (weight fraction data may be reported or predicted data,
     i.e., predicted from an ingredient list)"

    products.n
    "The number of products the chemical appears in, where a product is defined as a 
    product entry in Factotum." 
    """
    print('List of DTXSIDs provided:')
    print(dtxs)

    # pucs_n = DSSToxSubstance.objects.filter(sid__in=dtxs).distinct().\
    #     annotate(pucs_n=Count('ingredient__product__puc')).values('sid','pucs_n')
    # pucs_n = list(pucs_n)
    pucs_n = DSSToxSubstance.objects.filter(sid__in=dtxs).distinct().\
        annotate(pucs_n=Count('ingredient__product__puc')).values('sid','pucs_n')
    print('pucs_n:')
    print(pucs_n)

    dds_n = DSSToxSubstance.objects.filter(sid__in=dtxs).distinct().\
        annotate(dds_n=Count('ingredient__product__datadocument')).values('sid','dds_n')
    print('dds_n:')
    print(dds_n)

    dds_wf_n = DSSToxSubstance.objects\
    .filter(sid__in=dtxs).values('sid')\
    .annotate(
        dds_wf_n = Subquery(
            ExtractedChemical
            .objects
            .filter(pk=OuterRef('extracted_chemical_id') )
            .filter(
                Q(raw_max_comp__isnull=False) | 
                Q(raw_min_comp__isnull=False) | 
                Q(raw_central_comp__isnull=False)
            )
            .values('extracted_text_id')
            .distinct()
            .annotate(dds_wf_n=Count('extracted_text_id'))
            .values('dds_wf_n')
        )
    )
    print('dds_wf_n:')
    print(dds_wf_n)

    products_n = DSSToxSubstance.objects.filter(sid__in=dtxs).distinct().\
        annotate(products_n=Count('ingredient__product')).values('sid', 'products_n')
    print('products_n:')
    print(products_n)

    stats = pucs_n\
    .annotate(dds_n=Value(-1, output_field=IntegerField())) \
    .annotate(dds_wf_n=Value(-1, output_field=IntegerField())) \
    .annotate(products_n=Value(-1, output_field=IntegerField()))

    for row in stats:
        row['dds_n'] = dds_n.get(sid=row['sid'])['dds_n']
        row['dds_wf_n'] = dds_wf_n.get(sid=row['sid'])['dds_wf_n']
        row['products_n'] = products_n.get(sid=row['sid'])['products_n']

    return stats

def download_chem_stats(stats):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="chem_summary_metrics_%s.csv"' % (datetime.datetime.now().strftime("%Y%m%d"))

    writer = csv.writer(response)
    writer.writerow(['DTXSID', 'true_chemname', 'pucs_n', 'dds_n', 'dds_wf_n', 'products_n'])

    return response

def chem_stats_csv_view(request, pk, template_name='get_data/chem_summary_metrics.csv'):
    qs = DataDocument.objects.filter(data_group_id=pk)
    filename = DataGroup.objects.get(pk=pk).name
    return render_to_csv_response(qs, filename=filename, append_datestamp=True)