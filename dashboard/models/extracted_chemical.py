from django.db import models
from django.core.exceptions import ValidationError
from .extracted_text import ExtractedText


class ExtractedChemical(models.Model):
	UNITS_CHOICES = (
		('percent composition', 'percent composition'),
		('weight fraction', 'weight fraction'))

	extracted_text = models.ForeignKey(ExtractedText, on_delete=models.CASCADE)
	cas = models.CharField(max_length=50, null=True, blank=True)
	chem_name = models.CharField(max_length=500, null=True, blank=True)
	raw_min_comp = models.CharField(max_length=100, null=True, blank=True)
	raw_max_comp = models.CharField(max_length=100, null=True, blank=True)
	units = models.CharField(max_length=20, blank=True, choices=UNITS_CHOICES)
	report_funcuse = models.CharField(max_length=100, null=True, blank=True)

	def __str__(self):
		return self.chem_name
