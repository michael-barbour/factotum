from django.db import models
from .data_source import DataSource
from .data_document import DataDocument
from .source_category import SourceCategory
from django.utils import timezone
from django.core.urlresolvers import reverse


class Product(models.Model):
	data_source = models.ForeignKey(DataSource, on_delete=models.CASCADE)
	documents = models.ManyToManyField(DataDocument, through='ProductDocument')
	source_category = models.ForeignKey(SourceCategory, on_delete=models.CASCADE, null=True, blank=True)
	title = models.CharField(max_length=255)
	upc = models.CharField(db_index=True, max_length=60, null=False, blank=False, unique=True)
	url = models.CharField(max_length=500, null=True, blank=True)
	brand_name = models.CharField(db_index=True, max_length=200, null=True, blank=True)
	size = models.CharField(max_length=100, null=True, blank=True)
	model_number = models.CharField(max_length=200, null=True, blank=True)
	color = models.CharField(max_length=100, null=True, blank=True)
	item_id = models.IntegerField(null=True, blank=True)
	parent_item_id = models.IntegerField(null=True, blank=True)
	short_description = models.TextField(null=True, blank=True)
	long_description = models.TextField(null=True, blank=True)
	thumb_image = models.CharField(max_length=500, null=True, blank=True)
	medium_image = models.CharField(max_length=500, null=True, blank=True)
	large_image = models.CharField(max_length=500, null=True, blank=True)
	created_at = models.DateTimeField(default=timezone.now)
	updated_at = models.DateTimeField(null=True, blank=True)

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('product_edit', kwargs={'pk': self.pk})
