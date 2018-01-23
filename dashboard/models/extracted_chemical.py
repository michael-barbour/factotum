from django.db import models
from django.core.exceptions import ValidationError
from .extracted_text import ExtractedText


class ExtractedChemical(models.Model):
	UNITS_CHOICES = (
		('percent composition', 'percent composition'),
		('weight fraction', 'weight fraction'))

	extracted_text = models.ForeignKey(ExtractedText, on_delete=models.CASCADE)
	cas = models.CharField(max_length=200, null=True, blank=True)
	chem_name = models.CharField(max_length=100, null=True, blank=True)
	raw_min_comp = models.DecimalField(max_digits=20, decimal_places=15, blank=True, null=True)
	raw_max_comp = models.DecimalField(max_digits=20, decimal_places=15, blank=True)
	point_composition = models.DecimalField(max_digits=2, decimal_places=2, blank=True, null=True)
	units = models.CharField(max_length=20, blank=True, choices=UNITS_CHOICES)
	reported_functional_use = models.CharField(max_length=100, blank=True)

	def clean(self):
		if self.raw_min_comp is None and self.raw_max_comp is not None:
			raise ValidationError('raw_min_comp is required if raw_max_comp is provided.')
		if self.raw_max_comp is None and self.raw_min_comp is not None:
			raise ValidationError('raw_max_comp is required if raw_min_comp is provided.')