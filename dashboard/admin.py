from django.contrib import admin
from dashboard.models import *


# Register your models here.
admin.site.register(DataSource)
admin.site.register(DataGroup)
admin.site.register(SourceType)
admin.site.register(Product)
admin.site.register(SourceCategory)

