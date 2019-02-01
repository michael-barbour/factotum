from django.db import models
from .dsstox_lookup import DSSToxLookup
from model_utils.managers import InheritanceManager


class RawChem(models.Model):

    raw_cas = models.CharField("Raw CAS", max_length=100, null=True, blank=True)
    raw_chem_name = models.CharField("Raw chemical name", max_length=500,
                                                        null=True, blank=True)
    temp_id = models.IntegerField(default=0, null=True, blank=True)
    temp_obj_name = models.CharField(max_length=255, null=True, blank=True)

    rid = models.CharField(max_length=50, null=True, blank=True)

    dsstox = models.ForeignKey(DSSToxLookup, related_name = 'curated_chemical', on_delete=models.PROTECT,
                                                    null=True, blank=True)

    objects = InheritanceManager()

    def __str__(self):
        return self.raw_chem_name

    @property
    def sid(self):
        '''If there is no DSSToxLookup record via the 
        curated_chemical relationship, it evaluates to boolean False '''
        try:
            return self.curated_chemical.sid
        except AttributeError:
            return False



