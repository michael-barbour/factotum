from django.db import models
from django.utils import timezone
from django.core.urlresolvers import reverse


class DataGroup(models.Model):

	name = models.CharField(max_length=50)
	description = models.TextField(null=True, blank=True)
	downloaded_by = models.ForeignKey('auth.User', on_delete=models.CASCADE)
	downloaded_at = models.DateTimeField(default=timezone.now)
	extraction_script = models.CharField(max_length=250, null=True, blank=True)
	data_source = models.ForeignKey('DataSource', on_delete=models.CASCADE)
	updated_at = models.DateTimeField(default=timezone.now, null=True, blank=True)

	def __str__(self):
		return self.name

	def __unicode__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('data_group_edit', kwargs={'pk': self.pk})
