from django.db import models
from .common_info import CommonInfo
from .product import Product
from .product_attribute import ProductAttribute

class ProductToAttribute(CommonInfo):
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	product_attribute = models.ForeignKey(ProductAttribute, on_delete=models.CASCADE)

	def __str__(self):
		return self.id

