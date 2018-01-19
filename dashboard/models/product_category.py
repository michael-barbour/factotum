from django.db import models
from django.utils import timezone


class ProductCategory(models.Model):
	gen_cat = models.CharField(max_length=50, blank=False)
	prod_fam = models.CharField(max_length=50, null=True, blank=True)
	prod_type = models.CharField(max_length=100, null=True, blank=True)
	description = models.TextField(null=False, blank=False)
	created_at = models.DateTimeField(default=timezone.now)
	updated_at = models.DateTimeField(null=True, blank=True)
	last_edited_by = models.ForeignKey('auth.User', on_delete=models.CASCADE)

	def __str__(self):
		return self.gen_cat  # this may need to change

	class Meta:
		verbose_name_plural = 'Product categories'
