from django.db import models
from django.core.urlresolvers import reverse


class DataDocument(models.Model):

	filename = models.CharField(max_length=100)
	title = models.CharField(max_length=255)
	url = models.CharField(null=True, blank=True, max_length=200)
	product_category = models.CharField(null=True, blank=True, max_length=50)
	data_group = models.ForeignKey('DataGroup', on_delete=models.CASCADE)
	data_source = models.ForeignKey('DataSource', on_delete=models.CASCADE)
	products = models.ManyToManyField('Product', through='ProductDocument')
	matched = models.BooleanField(null=False, default=False)
	extracted = models.BooleanField(null=False, default=False)

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('data_document_edit', kwargs={'pk': self.pk})

	def get_download_script(self):
		return self__data_group.download_script
