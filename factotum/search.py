from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import DocType, Text, Date
from elasticsearch.helpers import bulk
from elasticsearch import Elasticsearch
from dashboard import models
from django.http import JsonResponse
from haystack.generic_views import FacetedSearchView as BaseFacetedSearchView
from haystack.query import SearchQuerySet
from factotum.forms import FacetedProductSearchForm

connections.create_connection()



class ProductIndex(DocType):
    title = Text()
    brand_name = Text(faceted=True)
    long_description = Text()
    short_description = Text()
    prod_cat = Text(faceted=True)
    upc = Text()
    model_number = Text()

    class Meta:
        index = 'product-index'
    
def bulk_indexing():

    ProductIndex.init()
    es = Elasticsearch()
    bulk(client=es, actions=(b.indexing() for b in models.Product.objects.all().iterator()))


class FacetedSearchView(BaseFacetedSearchView):

    form_class = FacetedProductSearchForm
    facet_fields = ['prod_cat', 'brand_name']
    template_name = 'search/facet_search.html'
    paginate_by = 3
    context_object_name = 'object_list'

