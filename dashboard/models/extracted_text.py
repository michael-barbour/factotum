from django.db import models
from .data_document import DataDocument


class ExtractedText(models.Model):
	data_document = models.ForeignKey(DataDocument, on_delete=models.CASCADE)
	doc_date = models.DateField(blank=True)
	rev_num = models.PositiveIntegerField(blank=True)
	extraction_script = models.ForeignKey('ExtractionScript', on_delete=models.CASCADE, default=1)
	qa_checked = models.BooleanField(default=False)

	def __str__(self):
		return self.id
