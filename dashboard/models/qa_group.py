from django.db import models
from .common_info import CommonInfo
from .extracted_text import ExtractedText
from .extracted_cpcat import ExtractedCPCat
from .script import Script


class QAGroup(CommonInfo):
    extraction_script = models.ForeignKey(Script,
                                    on_delete=models.CASCADE,
                                    blank=True, null=True,
                                    limit_choices_to={'script_type': 'EX'}, )
    extracted_cpcat = models.ForeignKey(ExtractedCPCat,
                                    on_delete=models.CASCADE,
                                    blank=True, null=True )
    qa_complete = models.BooleanField(default=False)

    def __str__(self):
        return str(self.extraction_script) + '_' + str(self.pk)

    def get_approved_doc_count(self):
        return ExtractedText.objects.filter(qa_group=self,
                                            qa_checked=True).count()
