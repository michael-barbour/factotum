from elasticsearch6 import Elasticsearch
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
import json
from dashboard.models import DataDocument, ExtractedChemical


@login_required
def search_chemicals(request, template_name='search/es_chemicals.html'):
    '''
    Returns both the raw elasticsearch results and the django objects 
    '''

    q = request.GET.get('q', '')
    es = Elasticsearch([
        {'host': 'localhost', 'port': 9400, 'use_ssl': False},
    ])
    results = es.search(index='factotum_chemicals', body={
        "query": {
            "query_string": {
                "query": q
            }
        }
    }
    )

    obj_results = []

    for hit in results['hits']['hits']:
        # print("%(raw_cas)s: %(raw_chem_name)s" % hit["_source"])
        # Reconstitute the django objects from the elasticsearch
        # json results
        obj_hit = {}
        obj_hit["dd"] = DataDocument.objects.get(
            pk=hit["_source"]["data_document_id"])
        obj_hit["raw_chem_name"] = hit["_source"]["raw_chem_name"]
        obj_hit["raw_cas"] = hit["_source"]["raw_cas"]
        obj_hit["true_cas"] = hit["_source"]["true_cas"]
        obj_hit["true_chemname"] = hit["_source"]["true_chemname"]
        obj_hit["product_count"] = hit["_source"]["product_count"]
        obj_results.append(obj_hit)

    context = {'results': results,
               'obj_results': obj_hits,
               'q': q,
               }
    return render(request, template_name, context)
