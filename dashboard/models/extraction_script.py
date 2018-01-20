from django.db import models
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.core.validators import URLValidator


class ExtractionScript(models.Model):

    title = models.CharField(max_length=50)
    url = models.TextField(null=True, blank=True, validators=[URLValidator()])

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('extraction_script_edit', kwargs={'pk': self.pk})

    def get_datadocument_count(self):
        return self.datadocument_set.count()

    def get_qa_complete_extractedtext_count(self):
        return self.datadocument_set.filter(extraction_script=self.pk, extractedtext__qa_done=True).count()

    def get_pct_checked(self):
        return 0
        