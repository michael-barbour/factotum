
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from dashboard.views import *
from dashboard.models import DataSource


@login_required()
def product_curation_index(request, template_name='product_curation/product_curation_index.html'):
	data_sources = DataSource.objects.all()
	for data_source in data_sources:
		data_source.uploaded = sum([len(d.datadocument_set.all()) for d in data_source.datagroup_set.all()])
		data_source.unlinked = data_source.uploaded - sum([len(x.datadocument_set.all()) for x in data_source.product_set.all()])

	return render(request, template_name, {'data_sources': data_sources})
