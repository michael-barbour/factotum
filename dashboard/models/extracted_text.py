from django.db import models
from django.core.exceptions import ValidationError

from .data_document import DataDocument
from .script import Script

class ExtractedText(models.Model):

	UNITS_CHOICES = (
		('percent composition','percent composition'),
		('weight fraction','weight fraction'))

	datadocument = models.ForeignKey(DataDocument, on_delete=models.CASCADE)
	cas = models.CharField(max_length=200, blank=True)
	chem_name = models.CharField(max_length=100, blank=True)
	raw_min_comp = models.DecimalField(max_digits=20,
									   decimal_places=15,
									   null=True,
									   blank=True)
	raw_max_comp = models.DecimalField(max_digits=20,
									   decimal_places=15,
									   null=True,
									   blank=True)
	units = models.CharField(max_length=2,
							 blank=True,
							 choices=UNITS_CHOICES)
	report_funcuse = models.CharField(max_length=100, blank=True)
	doc_date = models.DateField(blank=True, null=True)
	rev_num = models.IntegerField(blank=True, null=True)
	extraction_script = models.ForeignKey(Script,on_delete=models.CASCADE,
										limit_choices_to={'script_type': 'EX'},)

	def __str__(self):
		return self.datadocument.title

	def clean(self):
		if self.raw_min_comp is None and self.raw_max_comp is not None:
			raise ValidationError('raw_min_comp is required when raw_max_comp is provided.')
		if self.raw_max_comp is None and self.raw_min_comp is not None:
			raise ValidationError('raw_max_comp is required when raw_min_comp is provided.')
		if self.raw_min_comp and self.raw_max_comp:
			if self.raw_min_comp > self.raw_max_comp:
				raise ValidationError('raw_min_comp is greater than raw_max_comp.')
