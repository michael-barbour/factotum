from django.db import models
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.core.validators import URLValidator


class ExtractionScript(models.Model):

	title = models.CharField(max_length=50)
	url = models.TextField(null=True, blank=True, validators=[URLValidator()])

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('extraction_script_edit', kwargs={'pk': self.pk})
