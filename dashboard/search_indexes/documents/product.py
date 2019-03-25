from django_elasticsearch_dsl import DocType, Index, fields
from dashboard.models import Product, RawChem
from django.conf import settings

# ______              _            _       
# | ___ \            | |          | |      
# | |_/ / __ ___   __| |_   _  ___| |_ ___ 
# |  __/ '__/ _ \ / _` | | | |/ __| __/ __|
# | |  | | | (_) | (_| | |_| | (__| |_\__ \
# \_|  |_|  \___/ \__,_|\__,_|\___|\__|___/
                                         
                                
# Name of the Elasticsearch index
INDEX = Index(settings.ELASTICSEARCH_INDEX_NAMES[__name__])
# See Elasticsearch Indices API reference for available settings
INDEX.settings(
    number_of_shards=1,
    number_of_replicas=0
)

@INDEX.doc_type
class ProductDocument(DocType):


    class Meta:
        model = Product # The model associated with this DocType

        # The fields of the model you want to be indexed in Elasticsearch
        fields = [
            'title',
            'upc',
        ]



