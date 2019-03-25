from django_elasticsearch_dsl import DocType, Index, fields
from dashboard.models import Product, PUC
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

    facet_model_name = fields.KeywordField()

    def prepare_facet_model_name(self, instance):
        return "Product"

    pucs = fields.NestedField(properties={
        'gen_cat'  : fields.KeywordField(attr="puc.gen_cat"),
        'prod_fam' : fields.KeywordField(attr="puc.prod_fam"),
        'prod_type': fields.KeywordField(attr="puc.prod_type"),
    })

    # todo: add similar nested field for tags

    class Meta:
        model = Product # The model associated with this DocType

        # The fields of the model you want to be indexed in Elasticsearch
        fields = [
            'title',
            'upc',
            'short_description',
        ]
        related_models = [PUC]  # Optional: to ensure the Product will be re-saved when a PUC is updated


    def get_instances_from_related(self, related_instance):
        """If related_models is set, define how to retrieve the Car instance(s) from the related model.
        The related_models option should be used with caution because it can lead in the index
        to the updating of a lot of items.
        """
        if isinstance(related_instance, PUC):
            return related_instance.products.all()


