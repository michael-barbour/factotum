import datetime
from haystack import indexes
from dashboard.models import Product, DataDocument, PUC, ProductToPUC


class ProductIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.EdgeNgramField(
    document=True, use_template=True,
    template_name='search/indexes/dashboard/product_text.txt')
    title = indexes.EdgeNgramField(model_attr='title')
    facet_model_name = indexes.CharField(faceted=True)
    result_css_class = indexes.CharField()
    
    short_description = indexes.EdgeNgramField(model_attr="short_description", null=True)

    brand_name = indexes.CharField(
        model_attr='brand_name',
        faceted=True,
        null=True)

    pucs = indexes.MultiValueField(
        stored=True,
        faceted=True,
        null=True)
       

    def prepare_pucs(self, obj):
        return [puc.pk for puc in obj.puc_set.all()]
        #return obj.puc_set.all().values_list('pk', flat=True)


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
        return "Product"

    def prepare_result_css_class(self, obj):
        return "product-result"

class DataDocumentIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.EdgeNgramField(
    document=True, use_template=True,
    template_name='search/indexes/dashboard/data_document_text.txt')
    title            = indexes.EdgeNgramField(model_attr='title')
    facet_model_name = indexes.CharField(faceted=True)
    uploaded_at      = indexes.DateTimeField(model_attr='uploaded_at')
    result_css_class = indexes.CharField()
    
    filename = indexes.EdgeNgramField(model_attr="filename", null=True)

    def prepare_facet_model_name(self, obj):
        return "Data Document"
    
    def prepare_result_css_class(self, obj):
        return "datadocument-result"


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