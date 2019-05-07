from elasticsearch6 import Elasticsearch
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def search_chemicals(request, template_name='search/es_chemicals.html'):

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
    for hit in results['hits']['hits']:
        print("%(raw_cas)s: %(raw_chem_name)s" % hit["_source"])

    context = {'results': results,
                'q': q,
               }
    return render(request, template_name, context)
