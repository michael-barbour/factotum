from django.db import models
from django.utils import timezone


class WeightFractionType(models.Model):
	title = models.CharField(max_length=50)
	description = models.TextField(null=True, blank=True)
	created_at = models.DateTimeField(default=timezone.now)
	updated_at = models.DateTimeField(null=True, blank=True)

	def __str__(self):
		return self.title

	class Meta:
		ordering = ('id',)
