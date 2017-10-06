from django.db import models
from django.utils import timezone
from .source_type import SourceType

class DataSource(models.Model):
	title = models.CharField(max_length=50)
	url = models.CharField(max_length=150)
	type = models.ForeignKey(SourceType, on_delete=models.CASCADE)
	description = models.TextField(null=True, blank=True)
	created_at = models.DateTimeField(default=timezone.now)
	updated_at = models.DateTimeField(null=True, blank=True)

	def __str__(self):
		return self.title
