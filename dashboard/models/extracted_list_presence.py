from django.db import models

from dashboard.models import CommonInfo, ExtractedText

class ExtractedListPresence(CommonInfo):
    extracted_cpcat = models.ForeignKey('ExtractedCPCat', on_delete=models.CASCADE,
                                        related_name='presence')
    raw_cas = models.CharField("Raw CAS", max_length=100,
                                        null=True, blank=True)
    raw_chem_name = models.CharField("Raw chemical name", max_length=500,
                                        null=True, blank=True)

    def __str__(self):
        return self.raw_chem_name

    def get_datadocument_url(self):
        return self.extracted_cpcat.data_document.get_absolute_url()

    def get_extractedtext(self):
        return self.extracted_cpcat.extractedtext_ptr
