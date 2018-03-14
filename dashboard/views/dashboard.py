from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from dashboard.models import DataGroup, DataDocument, DataSource, Product
from django.db.models import Count, F
import datetime, time

current_date = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d')
select_upload_date = {"upload_date": """date(uploaded_at)"""}

@login_required(login_url='/login')
def index(request):
	stats = {}
	stats['datagroup_count'] = DataGroup.objects.count()
	stats['datasource_count'] = DataSource.objects.count()
	stats['datadocument_count'] = DataDocument.objects.count()
	stats['product_count'] = Product.objects.count()
	stats['product_with_puc_count'] = Product.objects.count()
	stats['documents_uploaded_count_by_date'] = document_uploaded_count_by_date()
	stats['document_percent_with_extracted_text_count'] = Product.objects.count()

	return render(request, 'dashboard/index.html', stats)

def document_uploaded_count_by_date():
	# Datasets to populate linechart with document-upload statistics
	# Number of datadocuments, both overall and by type, that have been uploaded as of each date
	document_stats = {}
	document_stats['all'] = list(DataDocument.objects.extra(select=select_upload_date) \
								 .values('upload_date') \
								 .annotate(document_count = Count('id')) \
								 .order_by('upload_date'))
	document_stats_by_type = DataDocument.objects.extra(select=select_upload_date) \
		.values('upload_date') \
		.annotate(source_type = F('data_group__data_source__type__title'), document_count = Count('id')) \
		.order_by('upload_date')
	document_stats['product'] = list(document_stats_by_type.filter(source_type = 'product'))
	document_stats['msds_sds'] = list(document_stats_by_type.filter(source_type = 'msds/sds'))
	for type in {'all', 'product', 'msds_sds'}:
		document_count = 0
		for item in document_stats[type]:
			if isinstance(item['upload_date'], datetime.date):
				item['upload_date'] = datetime.date.strftime((item['upload_date']), '%Y-%m-%d')
			document_count += item['document_count']
			item['document_count'] = document_count
		# if final record isn't for current date, create one
		for item in document_stats[type][len(document_stats[type])-1:]:
			if item['upload_date'] != current_date:
				document_stats[type].append({'upload_date': current_date
												, 'document_count': document_count})
	return document_stats
