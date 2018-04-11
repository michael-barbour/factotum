from django.db import models
from .extracted_chemical import ExtractedChemical
from django.utils import timezone
from django.core.urlresolvers import reverse


class DSSToxSubstance(models.Model):

    extracted_chemical = models.ForeignKey(ExtractedChemical, on_delete=models.CASCADE, null=False, blank=False)
    # TODO: confirm that deleting an ExtractedChemical should delete related DSSToxSubstance objects
    true_cas = models.CharField(max_length=50, null=True, blank=True)
    true_chemname = models.CharField(max_length=500, null=True, blank=True)
    rid = models.CharField(max_length=50, null=True, blank=True)
    sid = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.true_chemname

    def get_absolute_url(self):
        return reverse('dsstox_substance', kwargs={'pk': self.pk})
