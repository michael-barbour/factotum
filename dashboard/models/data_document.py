from django.db import models
from .common_info import CommonInfo
from django.urls import reverse
from django.utils import timezone
from .document_type import DocumentType
from django.core.exceptions import ValidationError


class DataDocument(CommonInfo):

    filename = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    url = models.CharField(null=True, blank=True, max_length=200)
    raw_category = models.CharField(null=True, blank=True, max_length=50)
    data_group = models.ForeignKey('DataGroup', on_delete=models.CASCADE)
    products = models.ManyToManyField('Product', through='ProductDocument')
    matched = models.BooleanField(default=False)
    extracted = models.BooleanField(default=False)
    document_type = models.ForeignKey(DocumentType, on_delete=models.PROTECT,
                                                        null=True, blank=True)
    organization = models.CharField(max_length=255, blank=True)
    note = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return str(self.title)

    @property
    def is_extracted(self):
        return hasattr(self,'extractedtext')

    def get_absolute_url(self):
        return reverse('data_document', kwargs={'pk': self.pk})

    def get_abstract_filename(self):
        ext = self.filename.split('.')[-1] #maybe not all are PDF??
        return f'document_{self.pk}.{ext}'

    def pdf_url(self):
        dg = self.data_group
        fn = self.get_abstract_filename()
        return f'/media/{dg.fs_id}/pdf/{fn}'

    def clean(self):
        # the document_type must be one of the children types
        # of the datadocument's parent datagroup
        this_type = self.data_group.group_type
        doc_types = DocumentType.objects.filter(group_type=this_type)
        if not self.document_type in doc_types:
            raise ValidationError(('The document type must be allowed by '
                                                    'the parent data group.'))

    def prep_for_cp_qa(self):
        from .extracted_cpcat import ExtractedCPCat
        from .extracted_list_presence import ExtractedListPresence
        import math
        from random import shuffle

        if not ExtractedCPCat.objects.filter(pk=self.pk).exists():
            ExtractedCPCat.objects.create(data_document=self, extraction_script_id=13)

        #total number of related listpresence objects
        list_presence_count = ExtractedListPresence.objects.filter(extracted_text=self.pk).count()

        if list_presence_count == 0:
            return

        non_qa_list_presence_ids = list(ExtractedListPresence.objects.filter(extracted_text=self.pk,
                                                         qa_flag=False
                                                         ).values_list('pk',
                                                                       flat=True))

        # total number of qa-flagged listpresence objects
        list_presence_qa_count = list_presence_count - len(non_qa_list_presence_ids)

        # if less than 30 records (or all records in set) flagged for QA, make up the difference
        if list_presence_qa_count < 30 and list_presence_qa_count < list_presence_count:
            random_x = 30 - list_presence_qa_count
            shuffle(non_qa_list_presence_ids)
            list_presence = ExtractedListPresence.objects.filter(pk__in=non_qa_list_presence_ids[:random_x])
            for lp in list_presence:
                lp.qa_flag = True
                lp.save()

        return
