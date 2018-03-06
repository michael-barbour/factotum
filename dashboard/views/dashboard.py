from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from dashboard.models import DataGroup, DataDocument, DataSource
from django.db.models import Count, F
import datetime, time


@login_required(login_url='/login')
def index(request):
	stats = {}
	stats['group_count'] = DataGroup.objects.count()
	stats['source_count'] = DataSource.objects.count()
	stats['document_count'] = DataDocument.objects.count()

	# Build datasets to populate linechart with document-upload statistics
	select_data = {"upload_date": """strftime('%%Y-%%m-%%d', uploaded_at)"""}
	# current_date = time.mktime(datetime.datetime.now().date().timetuple())
	current_date = datetime.datetime.now().strftime('%Y-%m-%d')
	document_stats = {}
	document_stats['all'] = list(DataDocument.objects.extra(select=select_data) \
								   .values('upload_date') \
								   .annotate(document_count = Count('id')) \
								   .order_by('upload_date'))
	document_stats_by_type = DataDocument.objects.extra(select=select_data) \
		.values('upload_date') \
		.annotate(source_type = F('data_group__data_source__type__title'), document_count = Count('id')) \
		.order_by('upload_date')
	document_stats['product'] = list(document_stats_by_type.filter(source_type = 'product'))
	document_stats['msds_sds'] = list(document_stats_by_type.filter(source_type = 'msds/sds'))
	for type in {'all', 'product', 'msds_sds'}:
		document_count = 0
		for item in document_stats[type]:
			# item['upload_date'] = datetime.datetime.strptime(item['upload_date'], "%Y-%m-%d").timestamp()
			document_count += item['document_count']
			item['document_count'] = document_count
		# if final record isn't for current date, create one
		for item in document_stats[type][len(document_stats[type])-1:]:
			if item['upload_date'] != current_date:
				document_stats[type].append({'upload_date': current_date
										  , 'document_count': document_count})
	stats['document_stats'] = document_stats

	return render(request, 'dashboard/index.html', stats)
