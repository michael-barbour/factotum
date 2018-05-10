from django.db import models
from .common_info import CommonInfo

class ProductCategory(CommonInfo):
	gen_cat = models.CharField(max_length=50, blank=False)
	prod_fam = models.CharField(max_length=50, null=True, blank=True)
	prod_type = models.CharField(max_length=100, null=True, blank=True)
	description = models.TextField(null=False, blank=False)
	last_edited_by = models.ForeignKey('auth.User', default = 1, on_delete=models.CASCADE)
	attribute = models.ForeignKey('ProductCategoryAttribute', on_delete=models.PROTECT)

	class Meta:
		ordering = ['gen_cat', 'prod_fam', 'prod_type']
		verbose_name_plural = 'Product categories'

	def __str__(self):
		return self.gen_cat + ' - ' + self.prod_fam + ' - ' + self.prod_type # this may need to change

	def natural_key(self):
		return self.gen_cat
