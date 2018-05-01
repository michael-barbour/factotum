from django.db import models
from .common_info import CommonInfo
from .ingredient import Ingredient
from .dsstox_substance import DSSToxSubstance


class DSSToxSubstanceIngredient(CommonInfo):
	dsstox_substance = models.ForeignKey(DSSToxSubstance, on_delete=models.CASCADE)
	ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)

	def __str__(self):
		return ""

