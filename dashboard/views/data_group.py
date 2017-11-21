from django.shortcuts import render, redirect, get_object_or_404
from django.forms import ModelForm
from django.contrib.auth.decorators import login_required
from dashboard.views import *
from datetime import datetime
from dashboard.models import DataGroup


class DataGroupForm(ModelForm):
	class Meta:
		model = DataGroup
		fields = ['name', 'description', 'downloaded_by', 'downloaded_at', 'extraction_script','data_source','updated_at']
	def __init__(self, *args, **kwargs):
		self.user = kwargs.pop('user', None)
		super(DataGroupForm, self).__init__(*args, **kwargs)

@login_required()
def data_group_list(request, template_name='data_group/datagroup_list.html'):
	datagroup = DataGroup.objects.all()
	data = {}
	data['object_list'] = datagroup
	return render(request, template_name, data)


@login_required()
def data_group_detail(request, pk, template_name='data_group/datagroup_detail.html'):
	datagroup = get_object_or_404(DataGroup, pk=pk, )
	return render(request, template_name, {'object': datagroup})


@login_required()
def data_group_create(request, template_name='data_group/datagroup_form.html'):
	#print(request.META)
	# get the data source from which the create button was clicked
	datasource_title = request.session['datasource_title']
	datasource_pk = request.session['datasource_pk']
	# get the highest data group id number associated with the data source, increment by 1
	new_group_key = DataGroup.objects.filter(data_source=datasource_pk).count() + 1
	default_name = '{} {}'.format(datasource_title, new_group_key)
	initial_values = {'downloaded_by': request.user, 'name': default_name, 'data_source':datasource_pk}
	form = DataGroupForm(request.POST or None, initial=initial_values)
	if request.method == 'POST':
		form = DataGroupForm(request.POST, user=request.user, \
		 initial=initial_values)
		if form.is_valid():
			# Do something with the data
			pass
	else:
		form = DataGroupForm(user=request.user, initial=initial_values)
	if form.is_valid():
		form.save()
		return redirect('data_group_list')
	return render(request, template_name, {'form': form})

@login_required()
def data_group_update(request, pk, template_name='data_group/datagroup_form.html'):
	datagroup = get_object_or_404(DataGroup, pk=pk)
	form = DataGroupForm(request.POST or None, instance=datagroup)
	if form.is_valid():
		datagroup.updated_at = datetime.now()
		form.save()
		return redirect('data_group_list')
	return render(request, template_name, {'form': form})


@login_required()
def data_group_delete(request, pk, template_name='data_source/datagroup_confirm_delete.html'):
	datagroup = get_object_or_404(DataGroup, pk=pk)
	if request.method == 'POST':
		datagroup.delete()
		return redirect('data_group_list')
	return render(request, template_name, {'object': datagroup})
