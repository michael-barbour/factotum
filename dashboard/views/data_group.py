from django.shortcuts import render, redirect, get_object_or_404
from django.forms import ModelForm
from django.contrib.auth.decorators import login_required
from dashboard.views import *
from datetime import datetime
from dashboard.models import DataGroup


class DataGroupForm(ModelForm):
	class Meta:
		model = DataGroup
		fields = ['name', 'description', 'downloaded_at', 'extraction_script','data_source','updated_at']

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
	form = DataGroupForm(request.POST or None)
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
