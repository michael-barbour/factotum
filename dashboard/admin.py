from dashboard.models import *
from django.contrib import admin


# auto-populate User field w/ current user
class ProductCategoryAdmin(admin.ModelAdmin):
    def get_changeform_initial_data(self, request):
        get_data = super(ProductCategoryAdmin, self).get_changeform_initial_data(request)
        get_data['last_edited_by'] = request.user.pk
        return get_data


# Register your models here.
admin.site.register(DataSource)
admin.site.register(DataGroup)
admin.site.register(DataDocument)
admin.site.register(Script)
admin.site.register(SourceType)
admin.site.register(Product)
admin.site.register(ProductDocument)
admin.site.register(SourceCategory)
admin.site.register(ProductCategory, ProductCategoryAdmin)
admin.site.register(ExtractedText)
admin.site.register(ExtractedChemical)
admin.site.register(DSSToxSubstance)
admin.site.register(QAGroup)
