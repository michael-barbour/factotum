import os
import shutil

from django.db import models
from .common_info import CommonInfo
from django.urls import reverse
from django.dispatch import receiver
from .group_type import GroupType


# could be used for dynamically creating filename on instantiation
# in the 'upload_to' param on th FileField
def update_filename(instance, filename):
    name_fill_space = instance.name.replace(' ', '_')
    name = '{0}/{0}_{1}'.format(name_fill_space, filename) # potential space errors in name
    return name


class DataGroup(CommonInfo):

    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    downloaded_by = models.ForeignKey('auth.User', on_delete=models.SET_DEFAULT, default = 1)
    downloaded_at = models.DateTimeField()
    download_script = models.ForeignKey('Script', on_delete=models.SET_NULL, default=None, null=True, blank=True)
    data_source = models.ForeignKey('DataSource', on_delete=models.CASCADE)
    csv = models.FileField(upload_to=update_filename, null=True)
    zip_file = models.CharField(max_length=100)
    group_type = models.ForeignKey(GroupType, on_delete=models.SET_DEFAULT, default=1, null=True, blank=True)
    url = models.CharField(max_length=150, blank=True)


    def matched_docs(self):
        return self.datadocument_set.filter(matched=True).count()

    def all_matched(self):
        return all(self.datadocument_set.values_list('matched', flat=True))

    def all_extracted(self):
        return all(self.datadocument_set.values_list('extracted', flat=True))

    def registered_docs(self):
        return self.datadocument_set.count()

    def extracted_docs(self):
        return self.datadocument_set.filter(extracted=True).count()

    def __str__(self):
        return self.name

    def dgurl(self):
        return self.name.replace(' ', '_')

    def get_absolute_url(self):
        return reverse('data_group_edit', kwargs={'pk': self.pk})

    def get_extracted_template_fieldnames(self):
        extract_fields = ['data_document_id','data_document_filename',
                            'prod_name', 'doc_date','rev_num', 'raw_category',
                            'raw_cas', 'raw_chem_name', 'report_funcuse']
        if self.group_type.title == 'Functional use':
            return extract_fields
        if self.group_type.title == 'Composition':
            return extract_fields + ['raw_min_comp','raw_max_comp', 'unit_type',
                                        'ingredient_rank', 'raw_central_comp']
        if self.group_type.title == 'Chemical presence list':
            for name in ['prod_name','rev_num','report_funcuse']:
                extract_fields.remove(name)
            return extract_fields + ['cat_code','description_cpcat',
                                    'cpcat_code','cpcat_sourcetype']

@receiver(models.signals.post_delete, sender=DataGroup)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes datagroup directory from filesystem
    when datagroup instance is deleted.
    """
    dg_folder = os.path.split(instance.csv.path)[0]
    if os.path.isdir(dg_folder):
        shutil.rmtree(dg_folder)
