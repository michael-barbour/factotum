from django.db import models
import math
from random import shuffle

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

    def create_qa_group(self):
        from .qa_group import QAGroup
        """
        Creates a QA Group for this ExtractedCPCat object;
        Use 10% of the related ExtractedListPresence records, with a maximum of 30
        """
        # Handle cases where a QA group already exists for the script
        if QAGroup.objects.filter(extracted_cpcat=self).count() == 1:
            # This is a valid state
            return QAGroup.objects.get(extracted_cpcat=self)
        elif QAGroup.objects.filter(extracted_cpcat=self).count() > 1:
            # this is a failure mode induced by the system's allowing
            # duplicate QA Groups to be created for a single script
            return QAGroup.objects.filter(extracted_cpcat=self).first()

        # Create a new QA Group for the ExtractionScript es
        qa_group = QAGroup.objects.create(extracted_cpcat=self)
        # Collect all the related ExtractedListPresence object keys that are related
        # to the DataDocument being QA'd and have not yet been checked
        list_presence_ids = list(ExtractedListPresence.objects.filter(extracted_text=self,
                                                         qa_flag=False
                                                         ).values_list('pk',
                                                                       flat=True))
        # If there are fewer than 100 related records, they make up the entire QA Group
        if len(list_presence_ids) < 100 and len(list_presence_ids) > 0:
            texts = ExtractedText.objects.filter(pk__in=list_presence_ids)
        # Otherwise sample 20 percent
        elif len(list_presence_ids) >= 100:
            # Otherwise sample 20% of them
            random_20 = math.ceil(len(list_presence_ids) / 5)
            shuffle(list_presence_ids)  # this is used to make random selection of texts
            texts = ExtractedText.objects.filter(pk__in=list_presence_ids[:random_20])
        else:
            # If there are no related ExtractedText records, something has gone wrong
            # Don't make a new QA Group with zero ExtractedTexts
            # print('The Script has no related ExtractedText records')
            texts = None

        # Set the qa_group attribute of each ExtractedText record to the new QA Group
        if texts is not None:
            for text in texts:
                text.qa_group = qa_group
                text.save()

        return qa_group
