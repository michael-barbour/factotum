from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import DocType, Date
from elasticsearch.helpers import bulk
from elasticsearch import Elasticsearch
from dashboard.models import Product, DataDocument, ExtractedChemical
from django.http import JsonResponse

