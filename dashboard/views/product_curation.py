from django.utils import timezone
from django.forms import ModelForm
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from dashboard.views import *
from dashboard.models import DataSource, DataDocument, Product, ProductDocument

class ProductForm(ModelForm):
	required_css_class = 'required' # adds to label tag
	class Meta:
		model = Product
		fields = ['title', 'brand_name']

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
		data_source.no_category = len(data_source.source.filter(prod_cat__isnull=True))
		# Number of data documents for each source which are NOT linked
		# to a product
		data_source.unlinked = (data_source.uploaded -
								sum([len(x.datadocument_set.all())
								for x in data_source.source.all()]))

	return render(request, template_name, {'data_sources': data_sources})

@login_required()
def category_assignment(request, pk, template_name=('product_curation/'
												'category_assignment.html')):
	"""Deliver a datasource and its associated products"""
	ds = DataSource.objects.get(pk=pk)
	products = ds.source.filter(prod_cat__isnull=True)
	for product in products:
		try:
			product.msds = product.datadocument_set.all()[0]
		except IndexError:
			product.msds = 0
	return render(request, template_name,{'datasource':ds, 'products':products})

@login_required()
def link_product_list(request,  pk, template_name='product_curation/link_product_list.html'):
	ds = DataSource.objects.get(pk=pk)

	unlinked_pks = list(set([dd.pk
							for dg in ds.datagroup_set.all()
							for dd in dg.datadocument_set.all()]
					  )-set([dd.pk
							for product in ds.source.all()
							for dd in product.datadocument_set.all()]))
	documents = DataDocument.objects.filter(pk__in=unlinked_pks)

	return render(request, template_name, {'documents':documents})

@login_required()
def link_product_form(request, pk, template_name=('product_curation/'
													'link_product_form.html')):
	doc = DataDocument.objects.get(pk=pk)
	form = ProductForm(request.POST or None)
	data_source_id = doc.data_group.data_source_id
	if request.method == 'POST':
		form = ProductForm(request.POST or None)
		if form.is_valid():
			title = form['title'].value()
			brand_name = form['brand_name'].value()
			try:
				product = Product.objects.get(title=title)
			except Product.DoesNotExist:
				upc_stub = ('stub_' +
							title +
							str(Product.objects.all().count() + 1))
				product = Product.objects.create(title         = title,
			 									brand_name     = brand_name,
												upc            = upc_stub,
												data_source_id = data_source_id,
												created_at     = timezone.now(),
												updated_at     = timezone.now())
			p = ProductDocument(product=product,document=doc)
			p.save()
		return redirect('link_product_list', pk=data_source_id)
	return render(request, template_name,{'document': doc,
											'form'  : form})

@login_required()
def assign_puc_to_product(request, pk, template_name=('product_curation/'
												'product_puc.html')):
	"""Assign a PUC to a single product"""
	p = Product.objects.get(pk=pk)
	return render(request, template_name,{'product':p})