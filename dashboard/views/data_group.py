import csv
from datetime import datetime
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.forms import ModelForm
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext_lazy as _
from django.core.files import File
from django.core.files.storage import FileSystemStorage
import os

from dashboard.views import *
from dashboard.models import DataGroup, DataDocument

class DataGroupForm(ModelForm):
	required_css_class = 'required' # adds to label tag
	class Meta:
		model = DataGroup
		fields = ['name', 'description', 'downloaded_by', 'downloaded_at', 'extraction_script','data_source','updated_at','csv']
		labels = {
            'csv': _('Register Records CSV File'),
        	}

	def __init__(self, *args, **kwargs):
		self.user = kwargs.pop('user', None)
		super(DataGroupForm, self).__init__(*args, **kwargs)
		self.fields['csv'].widget.attrs.update({'accept':'.csv'})

@login_required()
def data_group_list(request, template_name='data_group/datagroup_list.html'):
	datagroup = DataGroup.objects.all()
	data = {}
	data['object_list'] = datagroup
	return render(request, template_name, data)


@login_required()
def data_group_detail(request, pk,
						template_name='data_group/datagroup_detail.html'):
	datagroup = get_object_or_404(DataGroup, pk=pk, )
	docs = DataDocument.objects.filter(data_group_id=pk)
	err = False
	if request.method == 'POST':
		files = request.FILES.getlist('multifiles')
		# match filename to pdf name
		proc_files = [f for d in docs for f in files if f.name == d.filename]
		if not proc_files:
			err = True
		while proc_files:
			pdf = proc_files.pop(0)
			# set the Matched value of each registered record to True
			doc = DataDocument.objects.get(filename=pdf.name,
												data_group=datagroup.pk)
			if doc.matched: # skip if already matched
				continue
			doc.matched = True
			doc.save()
			# create the folder for the datagroup if it does not already exist
			fs = FileSystemStorage(settings.MEDIA_URL+str(datagroup.pk))
			fs.save(pdf.name, pdf)
	# refresh docs object if POST'd
	docs = DataDocument.objects.filter(data_group_id=pk)
	inc_upload = all([d.matched for d in docs])
	return render(request, template_name, {'datagroup'  : datagroup,
											'documents' : docs,
											'inc_upload': inc_upload,
											'err'       : err})

# raid_ant_killer.pdf
# raid_msds.pdf

@login_required()
def data_group_create(request, template_name='data_group/datagroup_form.html'):
	#print(request.META)
	# get the data source from which the create button was clicked
	datasource_title = request.session['datasource_title']
	datasource_pk = request.session['datasource_pk']
	# get the highest data group id number associated with the data source, increment by 1
	group_key = DataGroup.objects.filter(data_source=datasource_pk).count() + 1
	default_name = '{} {}'.format(datasource_title, group_key)
	initial_values = {'downloaded_by': request.user, 'name': default_name, 'data_source':datasource_pk}
	form = DataGroupForm(request.POST or None, initial=initial_values)
	if request.method == 'POST':
		form = DataGroupForm(request.POST, request.FILES, user=request.user, \
		 initial=initial_values)
		if form.is_valid():
			datagroup = form.save()
			print(datagroup.pk)
			info = [x.decode('ascii') for x in datagroup.csv.readlines()]
			table = csv.DictReader(info)
			if not table.fieldnames == ['filename','title','product','url']:
				datagroup.delete()
				return render(request, template_name,
								{'field_error': table.fieldnames,
									'form': form})
			text = ['DataDocument_id,' + ','.join(table.fieldnames)+'\n']
			errors = []
			count = 0
			for line in table: # read every csv line, create docs for each
				count+=1
				if line['filename'] == '':
					errors.append(count)
				if line['title'] == '': # updates title in line object
					line['title'] = line['filename'].split('.')[0]
				doc=DataDocument(filename=line['filename'],
								title=line['title'],
								product_category=line['product'],
								url=line['url'],
								data_group=datagroup)
				doc.save()
				# update line to hold the pk for writeout
				text.append(str(doc.pk)+','+ ','.join(line.values())+'\n')
			if errors:
				#datagroup.csv.close() # still need to close?? check
				datagroup.delete()
				return render(request, template_name, {'line_errors': errors,
														'form': form})
			with open(datagroup.csv.path,'w') as f:
			    myfile = File(f)
			    myfile.write(''.join(text))
			return redirect('data_group_detail', pk=datagroup.id)
	else:
		form = DataGroupForm(user=request.user, initial=initial_values)
	return render(request, template_name, {'form': form})

@login_required()
def data_group_update(request, pk):
	datagroup = get_object_or_404(DataGroup, pk=pk)
	form = DataGroupForm(request.POST or None, instance=datagroup)
	if form.is_valid():
		datagroup.updated_at = datetime.now()
		form.save()
		return redirect('data_group_list')
	return render(request, 'data_group/datagroup_form.html', {'form': form})


@login_required()
def data_group_delete(request, pk, template_name='data_source/datasource_confirm_delete.html'):
	datagroup = get_object_or_404(DataGroup, pk=pk)
	if request.method == 'POST':
		datagroup.delete()
		return redirect('data_group_list')
	return render(request, template_name, {'object': datagroup})
