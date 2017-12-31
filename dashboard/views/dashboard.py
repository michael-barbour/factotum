from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from dashboard.models import DataGroup, DataDocument, DataSource


# Create your views here.
@login_required(login_url='/login')
def index(request):
	group_count = DataGroup.objects.count()
	source_count = DataSource.objects.count()
	document_count = DataDocument.objects.count()
	stats = {}
	stats['group_count'] = group_count
	stats['source_count'] = source_count
	stats['document_count'] = document_count

	return render(request, 'dashboard/index.html', stats)


