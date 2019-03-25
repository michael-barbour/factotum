from django_elasticsearch_dsl import DocType, Index, fields
from dashboard.models import DataDocument
from django.conf import settings

# ______      _         ______                                      _       
# |  _  \    | |        |  _  \                                    | |      
# | | | |__ _| |_ __ _  | | | |___   ___ _   _ _ __ ___   ___ _ __ | |_ ___ 
# | | | / _` | __/ _` | | | | / _ \ / __| | | | '_ ` _ \ / _ \ '_ \| __/ __|
# | |/ / (_| | || (_| | | |/ / (_) | (__| |_| | | | | | |  __/ | | | |_\__ \
# |___/ \__,_|\__\__,_| |___/ \___/ \___|\__,_|_| |_| |_|\___|_| |_|\__|___/
                                                                          
                                                                         

# Name of the Elasticsearch index
INDEX = Index(settings.ELASTICSEARCH_INDEX_NAMES[__name__])
# See Elasticsearch Indices API reference for available settings
INDEX.settings(
    number_of_shards=1,
    number_of_replicas=0
)


@INDEX.doc_type
class DataDocumentDocument(DocType):

    facet_model_name = fields.KeywordField()

    def prepare_facet_model_name(self, instance):
        return "Data Document"

    class Meta:
        model = DataDocument # The model associated with this DocType

        # The fields of the model you want to be indexed in Elasticsearch
        fields = [
            'filename',
            'title',
            'url',
        ]

        # Ignore auto updating of Elasticsearch when a model is saved
        # or deleted:
        # ignore_signals = True
        # Don't perform an index refresh after every update (overrides global setting):
        # auto_refresh = False
        # Paginate the django queryset used to populate the index with the specified size
        # (by default there is no pagination)
        # queryset_pagination = 5000

