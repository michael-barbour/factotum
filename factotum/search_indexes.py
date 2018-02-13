import datetime
from haystack import indexes
from dashboard.models import Product, DataDocument, ProductCategory


class ProductIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.EdgeNgramField(
    document=True, use_template=True,
    template_name='search/indexes/dashboard/product_text.txt')
    title = indexes.EdgeNgramField(model_attr='title')
    facet_model_name = indexes.CharField(faceted=True)
    
    short_description = indexes.EdgeNgramField(model_attr="short_description", null=True)

    brand_name = indexes.CharField(
        model_attr='brand_name',
        faceted=True)

    prod_cat = indexes.CharField(
        model_attr='prod_cat',
        faceted=True)

# The document type can't be properly indexed until it's added here:
# https://github.com/HumanExposure/factotum/issues/125   
#    document_type = indexes.CharField(
#        model_attr='document_type',
#        faceted=True)

    def get_model(self):
        return Product

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()

    def prepare_facet_model_name(self, obj):
        return "product"

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