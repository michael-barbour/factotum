from django.db import models
from .common_info import CommonInfo
from datetime import datetime
from django.core.exceptions import ValidationError
from .data_document import DataDocument
from .script import Script


class ExtractedText(CommonInfo):
    data_document = models.OneToOneField(DataDocument,on_delete=models.CASCADE,
                                                            primary_key=True)
    record_type = models.CharField(max_length=50, null=True, blank=True)
    prod_name = models.CharField(max_length=500, null=True, blank=True)
    doc_date = models.CharField(max_length=10, null=True, blank=True)
    rev_num = models.CharField(max_length=50, null=True, blank=True)
    extraction_script = models.ForeignKey(
        Script, on_delete=models.CASCADE, limit_choices_to={'script_type': 'EX'}, )
    qa_checked = models.BooleanField(default=False)
    APPROVED_WITH_ERROR = "APPROVED_WITH_ERROR"
    APPROVED_WITHOUT_ERROR = "APPROVED_WITHOUT_ERROR"
    APPROVAL_CHOICES = (
        (APPROVED_WITHOUT_ERROR, "Approved without errors"),
        (APPROVED_WITH_ERROR, "Approved with errors")
    )
    qa_status = models.CharField(max_length=30,
                                 choices=APPROVAL_CHOICES,
                                 default=None,
                                 blank=True,
                                 null=True)
    qa_approved_date = models.DateTimeField(null=True, blank=True)
    qa_approved_by = models.ForeignKey(
        'auth.User', null=True, blank=True, on_delete=models.SET_NULL)
    qa_group = models.ForeignKey('QAGroup', null=True, blank=True,
                                 on_delete=models.SET_NULL)
    qa_notes = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return str(self.prod_name)

    def next_extracted_text_in_qa_group(self):
        extextnext = get_next_or_prev(ExtractedText.objects.filter(
            qa_group=self.qa_group, qa_checked=False), self, 'next')
        if extextnext:
            # Replace our item with the next one
            nextid = extextnext.pk
        if extextnext == self:
            nextid = 0
        return nextid

    def clean(self):
        return data
        if self.doc_date:
            if len(self.doc_date) != 10:
                raise ValidationError("Date format is the wrong length.")
            if self.doc_date[4] != '-' or self.doc_date[7] != '-':
                raise ValidationError(('Date format is off, '
                                      'should be  YYYY-MM-DD.'))
            try:
                int(self.doc_date[:4])
                int(self.doc_date[5:7])
                int(self.doc_date[8:10])
            except ValueError:
                raise ValidationError("Date is off.")
            if not int(self.doc_date[:4]) <= datetime.now().year:
                raise ValidationError('Date is off, year is invalid.')
            if not int(self.doc_date[5:7]) in range(1, 13):
                raise ValidationError('Date is off, month is invalid.')
            if not int(self.doc_date[8:10]) in range(1, 32):
                raise ValidationError('Date is off, day is invalid.')


def get_next_or_prev(models, item, direction):
    '''
    Returns the next or previous item of
    a query-set for 'item'.

    'models' is a query-set containing all
    items of which 'item' is a part of.

    direction is 'next' or 'prev'

    '''
    getit = False
    if direction == 'prev':
        models = models.reverse()
    for m in models:
        if getit:
            return m
        if item == m:
            getit = True
    if getit:
        # This would happen when the last
        # item made getit True
        return models[0]
    return False
