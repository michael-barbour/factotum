from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from dashboard.models import (ExtractedChemical, ExtractedText, ProductDocument,
                              DSSToxSubstance, Product)

def index(request, slug):
    #print(slug)
    #chem = get_object_or_404(DSSToxSubstance, sid=slug)
    b = ExtractedChemical.objects.filter(dsstoxsubstance__sid=slug)
    r = ExtractedText.objects.filter(extractedchemical__in=b).values_list('pk',
                                                                      flat=True)
    p = ProductDocument.objects.filter(document_id__in=r)
    products = list(Product.objects.filter(pk__in=p).values())
    # Product.objects.values('title','brand_name','manufacturer','upc','size')
    # products = list(Product.objects.values())
    return JsonResponse(products, safe=False)
