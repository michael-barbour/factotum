from django.db import models
from .extracted_text import ExtractedText
from .extracted_list_presence import ExtractedListPresence


class ExtractedCPCat(ExtractedText):
    cat_code = models.CharField("Cat Code", max_length=100,
                                        null=True, blank=True)
    description_cpcat = models.CharField("Description CPCat", max_length=200,
                                        null=True, blank=True)
    cpcat_code = models.CharField("CPCat Code", max_length=50,
                                        null=True, blank=True)
    cpcat_sourcetype = models.CharField("CPCat SourceType", max_length=50,
                                        null=True, blank=True)

    def __str__(self):
        return str(self.prod_name)

    def prep_for_cp_qa(self):
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
