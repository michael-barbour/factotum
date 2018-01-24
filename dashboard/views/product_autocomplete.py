from dal import autocomplete
from dashboard.models import Product, ProductCategory


class PUCAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated():
            return ProductCategory.objects.none()
        qs = ProductCategory.objects.all()
        if self.q:
            qs = qs.filter(gen_cat__istartswith=self.q)

        return qs
