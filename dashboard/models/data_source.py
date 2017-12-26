from django.db import models
from django.utils import timezone
from .source_type import SourceType
from django.core.urlresolvers import reverse

class DataSource(models.Model):
	STATE_CHOICES = (
					('AT','Awaiting Triage'),
					('IP','In Progress'),
					('CO','Complete'),
					('ST','Stale'))

	PRIORITY_CHOICES = (
						('HI', 'High'),
						('MD', 'Medium'),
						('LO', 'Low')
						)

	title = models.CharField(max_length=50)
	url = models.CharField(max_length=150)
	estimated_records = models.PositiveIntegerField(default=0)
	type = models.ForeignKey(SourceType, on_delete=models.CASCADE)
	state = models.CharField(max_length=2,
							choices=STATE_CHOICES,
							default='AT')

	description = models.TextField(null=True, blank=True)
	created_at = models.DateTimeField(default=timezone.now)
	updated_at = models.DateTimeField(null=True, blank=True)
	priority = models.CharField(max_length=2,
							choices=PRIORITY_CHOICES,
							default='HI')

	def __str__(self):
		return self.title

	def __unicode__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('data_source_edit', kwargs={'pk': self.pk})
