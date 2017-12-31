from django.db import models
from .product import Product
from .data_document import DataDocument
from django.utils import timezone


class ProductDocument(models.Model):
	upc = models.CharField(db_index=True, max_length=40, null=False, blank=False, unique=True)
	product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
	document = models.ForeignKey(DataDocument, on_delete=models.CASCADE)

	created_at = models.DateTimeField(default=timezone.now)
	updated_at = models.DateTimeField(null=True, blank=True)

	def __str__(self):
		return self.upc

	def __unicode__(self):
		return self.upc

	def get_absolute_url(self):
		return reverse('product_edit', kwargs={'pk': self.pk})
