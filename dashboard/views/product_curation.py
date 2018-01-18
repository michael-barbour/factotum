from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from dashboard.views import *
from dashboard.models import DataSource, DataDocument


@login_required()
def product_curation_index(request, template_name='product_curation/product_curation_index.html'):
	# List of all data sources which have had at least 1 data
	# document matched to a registered record
	docs = DataDocument.objects.all()
	valid_ds = set([d.data_group.data_source_id for d in docs])
	data_sources = DataSource.objects.filter(pk__in=valid_ds)

	for data_source in data_sources:
		# Number of data documents which have been matched for each source
		data_source.uploaded = sum([len(d.datadocument_set.all()) for d in data_source.datagroup_set.all()])
		# Number of data documents for each source which are NOT linked
		# to a product
		# TODO data_source.unlinked = data_source.uploaded - sum([len(x.datadocument_set.all()) for x in data_source.product_set.all()])

	return render(request, template_name, {'data_sources': data_sources})
