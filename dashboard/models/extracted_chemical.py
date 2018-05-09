from django.db import models
from .common_info import CommonInfo
from django.core.exceptions import ValidationError
from .extracted_text import ExtractedText
from .unit_type import UnitType
from .weight_fraction_type import WeightFractionType

def validate_ingredient_rank(value):
	if value < 1 or value > 999:
		raise ValidationError(
			('Quantity {} is not allowed'.format(value)),params={'value': value},
		)


class ExtractedChemical(CommonInfo):
	extracted_text = models.ForeignKey(ExtractedText, on_delete=models.CASCADE, related_name='chemicals')
	raw_cas = models.CharField(max_length=50, null=True, blank=True)
	raw_chem_name = models.CharField(max_length=500, null=True, blank=True)
	raw_min_comp = models.CharField(max_length=100, null=True, blank=True)
	raw_max_comp = models.CharField(max_length=100, null=True, blank=True)
	unit_type = models.ForeignKey(UnitType, on_delete=models.PROTECT)
	report_funcuse = models.CharField(max_length=100, null=True, blank=True)
	weight_fraction_type = models.ForeignKey(WeightFractionType, on_delete=models.PROTECT, null=True, default='1')
	ingredient_rank = models.PositiveIntegerField(null=True, blank=True, validators=[validate_ingredient_rank])
	raw_central_comp = models.CharField(max_length=100, null=True, blank=True)

	def __str__(self):
		return self.raw_chem_name