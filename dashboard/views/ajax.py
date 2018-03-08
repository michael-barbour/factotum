from django.http import HttpResponse
from django.core import serializers
from dashboard.models import DataGroup, Product

def DataGroups_asJson(request):
    object_list = DataGroup.objects.all() 
    json = serializers.serialize('json', object_list)
    return HttpResponse(json, content_type='application/json')

def Products_asJson(request):
    object_list = Product.objects.all() 
    json = serializers.serialize('json', object_list)
    return HttpResponse(json, content_type='application/json')

