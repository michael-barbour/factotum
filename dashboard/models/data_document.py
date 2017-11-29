from django.db import models
from django.utils import timezone
from django.core.urlresolvers import reverse


class DataDocument(models.Model):

	PCAT_CHOICES = (
	('','Uncategorized'),
	('cleaner','cleaner'),
	('lawn treatment','lawn treatment'),
    ('hair care','hair care')
    )

	title = models.CharField(max_length=600)
	url = models.CharField(null=True, blank=True, max_length=600)
	product_category = models.CharField(max_length=2,
							choices=PCAT_CHOICES,
							default='')
	data_group = models.ForeignKey('DataGroup', on_delete=models.CASCADE)
	matched    = models.BooleanField(default=False)
	extracted    = models.BooleanField(default=False)

	def __str__(self):
		return self.title

	def __unicode__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('data_document_edit', kwargs={'pk': self.pk})
