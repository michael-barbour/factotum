from django.db import models
from .data_document import DataDocument


class ExtractedText(models.Model):
	data_document = models.ForeignKey(DataDocument, on_delete=models.CASCADE)
	doc_date = models.DateField(blank=True)
	rev_num = models.PositiveIntegerField(blank=True)

	def __str__(self):
		return self.id
