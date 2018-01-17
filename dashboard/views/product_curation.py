
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from dashboard.views import *
from dashboard.models import DataSource, DataDocument, Product


@login_required()
def product_curation_index(request, template_name='product_curation/product_curation_index.html'):
	# List of all data sources which have had at least 1 data
	# document matched to a registered record
	docs = DataDocument.objects.all()
	valid_ds = set([d.data_group.data_source_id for d in docs])
	data_sources = DataSource.objects.filter(pk__in=valid_ds)

	for data_source in data_sources:
		# Number of data documents which have been matched for each source
		data_source.uploaded = sum([len(d.datadocument_set.all())
								for d in data_source.datagroup_set.all()])
		# Number of data documents for each source which are NOT linked
		# to a product
		data_source.unlinked = (data_source.uploaded -
								sum([len(x.datadocument_set.all())
								for x in data_source.product_set.all()]))

	return render(request, template_name, {'data_sources': data_sources})

@login_required()
def link_product_list(request,  pk, template_name='product_curation/link_product_list.html'):
	ds = DataSource.objects.get(pk=pk)
	products = Product.objects.filter(data_source=ds)
	[dd.pk for p in products for dd in p.datadocument_set.all()]



	# list(set([dd.pk for dg in ds.datagroup_set.all() for dd in dg.datadocument_set.all()])-set([dd.pk for product in ds.product_set.all() for dd in product.datadocument_set.all()]))

	unlinked_pks = list(set([dd.pk
							for dg in ds.datagroup_set.all()
							for dd in dg.datadocument_set.all()]
					  )-set([dd.pk
							for product in ds.product_set.all()
							for dd in product.datadocument_set.all()]))
	documents = DataDocument.objects.filter(pk__in=unlinked_pks)

	return render(request, template_name, {'documents':documents})

# len([d
# for d in docs
# if d.data_group.data_source_id == datasource.pk
# and d.matched ==True
# ])/float(datasource.estimated_records))*100
