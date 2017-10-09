from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^datasources/$', views.DataSourceList.as_view(), name='data_source_list'),
	url(r'^datasource/(?P<pk>\d+)$', views.DataSourceDetail.as_view(), name='data_source_detail'),
	url(r'^datasource/new$', views.DataSourceCreate.as_view(), name='data_source_new'),
	url(r'^datasource/edit/(?P<pk>\d+)$', views.DataSourceUpdate.as_view(), name='data_source_edit'),
	url(r'^datasource/delete/(?P<pk>\d+)$', views.DataSourceDelete.as_view(), name='data_source_delete'),
]