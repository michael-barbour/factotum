from django.http import HttpResponse, JsonResponse
from dashboard.models import Product
from django.db.models import Q


def product_ajax(request):

    columns = [
        "title",
        "brand_name",
        "id"
    ]
    start = int(request.GET.get("start", 0))
    length = int(request.GET.get("length", 10))
    order_column = int(request.GET.get("order[0][column]", 0))
    order_direction = "-" if request.GET.get("order[0][dir]", "asc") == "desc" else ""
    order_column_name = columns[order_column]
    global_search = request.GET.get("search[value]", "")
    all_objects = Product.objects.all()
    if global_search:
        all_objects = all_objects.filter(
                Q(title__contains=global_search) |
                Q(brand_name__contains=global_search)
        )

    objects = []
    for i in all_objects.order_by(order_direction + order_column_name)[
        start : start + length
    ].values():
        ret = [i[j] for j in columns]
        objects.append(ret)

    filtered_count = all_objects.count()
    total_count = Product.objects.count()
    return JsonResponse(
        {
            "recordsTotal": total_count,
            "recordsFiltered": filtered_count,
            "data": objects,
        }
    )
