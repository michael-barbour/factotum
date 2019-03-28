from django.db import models
from .common_info import CommonInfo
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from dashboard.models import ExtractedText


class QANotes(CommonInfo):
    extracted_text = models.OneToOneField(ExtractedText, on_delete=models.CASCADE)
    qa_notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return 'Notes for {}'.format(self.extracted_text)

    def clean(self):
        if self.extracted_text.qa_edited and not self.qa_notes:
            raise ValidationError(
                    _('Before approving, please add a note explaining your edits to the extracted data'))
