from django.db import models

from dashboard.models import CommonInfo
from .raw_chem import RawChem

class ExtractedListPresence(CommonInfo, RawChem):
                                        
    rawchem_ptr = models.OneToOneField(blank=False, null=False, 
            related_name='extracted_listpresence',parent_link=True ,
            on_delete=models.CASCADE, to='dashboard.RawChem')

    @classmethod
    def detail_fields(cls):
        return ['raw_cas','raw_chem_name']

    def __str__(self):
        return str(self.raw_chem_name) if self.raw_chem_name else ''

    def get_datadocument_url(self):
        return self.extracted_cpcat.data_document.get_absolute_url()

    def get_extractedtext(self):
        return self.extracted_cpcat.extractedtext_ptr
    
    @property
    def data_document(self):
        return self.extracted_text.data_document
