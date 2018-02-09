import datetime
from haystack import indexes
from dashboard.models import DataDocument, DataGroup, Product, ProductCategory


class ProductIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.EdgeNgramField(
    document=True, use_template=True,
    template_name='search/indexes/dashboard/product_text.txt')
    title = indexes.EdgeNgramField(model_attr='title')
    
    short_description = indexes.EdgeNgramField(model_attr="short_description", null=True)

    brand_name = indexes.CharField(
        model_attr='brand_name',
        faceted=True)

    prod_cat = indexes.CharField(
        model_attr='prod_cat',
        faceted=True)
    
    source_category = indexes.CharField(
        model_attr='source_category',
        faceted=True)

    def get_model(self):
        return Product

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()