from django_elasticsearch_dsl import DocType, Index, fields
from dashboard.models import DataDocument, RawChem
from django.conf import settings

#  _____ _                    _           _     
# /  __ \ |                  (_)         | |    
# | /  \/ |__   ___ _ __ ___  _  ___ __ _| |___ 
# | |   | '_ \ / _ \ '_ ` _ \| |/ __/ _` | / __|
# | \__/\ | | |  __/ | | | | | | (_| (_| | \__ \
#  \____/_| |_|\___|_| |_| |_|_|\___\__,_|_|___/
                                              
                          
# Name of the Elasticsearch index
INDEX = Index(settings.ELASTICSEARCH_INDEX_NAMES[__name__])
# See Elasticsearch Indices API reference for available settings
INDEX.settings(
    number_of_shards=1,
    number_of_replicas=0
)

@INDEX.doc_type
class FactotumChemicalDocument(DocType):

    facet_model_name = fields.KeywordField()
    data_document_id = fields.IntegerField()
    product_count = fields.IntegerField()
    raw_cas = fields.KeywordField()

    def prepare_facet_model_name(self, instance):
        return "Chemical"

    def prepare_raw_cas(self, instance):
        return instance.raw_cas

    def prepare_data_document_id(self, instance):
        return instance.extracted_text.data_document.id
    
    def prepare_product_count(self, instance):
        return instance.extracted_text.data_document.product_set.count()

    dsstox = fields.ObjectField(properties={
        'true_cas': fields.KeywordField(),
        'true_chemname': fields.KeywordField(),
    })
    class Meta:
        model = RawChem # The model associated with this DocType

        # The fields of the model you want to be indexed in Elasticsearch
        fields = [
            'raw_chem_name',
        ]

    def get_queryset(self):
        """Not mandatory but to improve performance we can select related in one sql request"""
        return super(FactotumChemicalDocument, self).get_queryset().select_related(
            'dsstox'
        )

    def get_instances_from_related(self, related_instance):
        """If related_models is set, define how to retrieve the RawChem instance(s) from the related model.
        The related_models option should be used with caution because it can lead in the index
        to the updating of a lot of items.
        """
        if isinstance(related_instance, DSSToxLookup):
            return related_instance.rawchem_set.all()


