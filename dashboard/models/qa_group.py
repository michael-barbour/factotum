from django.db import models
from .script import Script
from django.utils import timezone



class QAGroup(models.Model):

	extraction_script = models.ForeignKey(Script,
									on_delete=models.CASCADE,
									limit_choices_to={'script_type': 'EX'}, )
	created_at = models.DateTimeField(default=timezone.now)
	updated_at = models.DateTimeField(null=True, blank=True)

	def __str__(self):
		return str(self.extraction_script) + '_' + str(self.pk)
