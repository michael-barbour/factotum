from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from dashboard.models import DataSource
from django.contrib.auth.mixins import LoginRequiredMixin


class DataSourceList(LoginRequiredMixin, ListView):
	model = DataSource
	login_url = '/login/'
	redirect_field_name = 'redirect_to'


class DataSourceDetail(LoginRequiredMixin, DetailView):
	model = DataSource
	login_url = '/login/'
	redirect_field_name = 'redirect_to'


class DataSourceCreate(LoginRequiredMixin, CreateView):
	model = DataSource
	success_url = reverse_lazy('data_source_list')
	fields = ['title', 'url', 'created_at']
	login_url = '/login/'
	redirect_field_name = 'redirect_to'


class DataSourceUpdate(LoginRequiredMixin, UpdateView):
	model = DataSource
	success_url = reverse_lazy('data_source_list')
	fields = ['title', 'url', 'description']
	login_url = '/login/'
	redirect_field_name = 'redirect_to'


class DataSourceDelete(LoginRequiredMixin, DeleteView):
	model = DataSource
	success_url = reverse_lazy('data_source_list')
	login_url = '/login/'
	redirect_field_name = 'redirect_to'
