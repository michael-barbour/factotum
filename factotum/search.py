from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import DocType, Text, Date
from elasticsearch.helpers import bulk
from elasticsearch import Elasticsearch
from dashboard import models

connections.create_connection()

class ProductIndex(DocType):
    title = Text()
    brand_name = Text()
    long_description = Text()
    short_description = Text()

    class Meta:
        index = 'product-index'

def bulk_indexing():
    ProductIndex.init()
    es = Elasticsearch()
    bulk(client=es, actions=(b.indexing() for b in models.Product.objects.all().iterator()))