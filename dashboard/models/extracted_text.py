from django.db import models
from django.core.exceptions import ValidationError

from .data_document import DataDocument
from .script import Script

class ExtractedText(models.Model):

	data_document = models.ForeignKey(DataDocument, on_delete=models.CASCADE)
	record_type = models.CharField(max_length=50, null=True, blank=True)
	prod_name = models.CharField(max_length=500, null=True, blank=True)
	doc_date = models.CharField(max_length=10, null=True, blank=True)
	rev_num = models.CharField(max_length=50, null=True, blank=True)
	extraction_script = models.ForeignKey(Script,on_delete=models.CASCADE,
										limit_choices_to={'script_type': 'EX'},)

	def __str__(self):
		return self.datadocument.title

	def clean(self):
		if self.doc_date[4] == '-' and self.doc_date[7] == '-':
			raise ValidationError('Date format is off, should be  YYYY-MM-DD.')
