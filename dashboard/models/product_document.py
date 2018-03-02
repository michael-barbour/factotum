from django.db import models
from .product import Product
from .data_document import DataDocument
from django.utils import timezone


class ProductDocument(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
	document = models.ForeignKey(DataDocument, on_delete=models.CASCADE)

	created_at = models.DateTimeField(default=timezone.now)
	updated_at = models.DateTimeField(null=True, blank=True)

	def __str__(self):
		return self.product.title

	def get_absolute_url(self):
		return reverse('product_detail', kwargs={'pk': self.pk})
