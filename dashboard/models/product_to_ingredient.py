from django.db import models
from .common_info import CommonInfo
from .product import Product
from .ingredient import Ingredient


class ProductToIngredient(CommonInfo):
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)

	def __str__(self):
		return self.id

