from django.db import models
from .data_source import DataSource
from django.utils import timezone
from django.core.urlresolvers import reverse


class SourceCategory(models.Model):
	data_source = models.ForeignKey(DataSource, on_delete=models.CASCADE)
	title = models.CharField(max_length=200, null=False, blank=False)
	source_id = models.CharField(max_length=255, null=True, blank=True)
	source_parent_id = models.CharField(max_length=255, null=True, blank=True)
	path = models.CharField(max_length=255, null=True, blank=True)

	created_at = models.DateTimeField(default=timezone.now)
	updated_at = models.DateTimeField(null=True, blank=True)

	def __str__(self):
		return self.data_source.title + ', ' + self.path

	def get_absolute_url(self):
		return reverse('source_category_edit', kwargs={'pk': self.pk})

	class Meta:
		verbose_name_plural = 'Source categories'
