from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import DocType, Text, Date
from elasticsearch.helpers import bulk
from elasticsearch import Elasticsearch
from dashboard import models
from django.http import JsonResponse
from haystack.generic_views import FacetedSearchView as BaseFacetedSearchView
from haystack.query import SearchQuerySet
from factotum.forms import FacetedProductSearchForm
from haystack import indexes


connections.create_connection()



class ProductIndex(DocType):
    title = Text()
    brand_name = Text(faceted=True)
    long_description = Text()
    short_description = Text()
    prod_cat = Text(faceted=True)
    upc = Text()
    model_number = Text()
    source_category=Text(faceted=True)

    class Meta:
        index = 'product-index'

# 
# 
# 
# 
#    
class DataDocumentIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.EdgeNgramField(
    document=True, use_template=True,
    template_name='search/indexes/dashboard/product_text.txt')
    title = indexes.EdgeNgramField(model_attr='title')
    facet_model_name = indexes.CharField(faceted=True)
    
    filename = indexes.EdgeNgramField(model_attr="filename", null=True)

    def prepare_facet_model_name(self, obj):
        return "datadocument"


# The document type can't be properly indexed until it's added here:
# https://github.com/HumanExposure/factotum/issues/125   
#    document_type = indexes.CharField(
#        model_attr='document_type',
#        faceted=True)

    def get_model(self):
        return DataDocument

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()






def bulk_indexing():

    ProductIndex.init()
    es = Elasticsearch()
    bulk(client=es, actions=(b.indexing() for b in models.Product.objects.all().iterator()))


class FacetedSearchView(BaseFacetedSearchView):

    form_class = FacetedProductSearchForm
    facet_fields = ['prod_cat', 'brand_name','facet_model_name']
    template_name = 'search/facet_search.html'
    paginate_by = 10
    context_object_name = 'object_list'

