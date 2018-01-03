import os
import shutil

from django.db import models
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.dispatch import receiver

# could be used for dynamically creating filename on instantiation
# in the 'upload_to' param on th FileField
def update_filename(instance, filename):
	name_fill_space = instance.name.replace(' ','_')
	name = '{0}/{0}_{1}'.format(name_fill_space,filename) # potential space errors in name
	return name


class DataGroup(models.Model):

	name = models.CharField(max_length=50)
	description = models.TextField(null=True, blank=True)
	downloaded_by = models.ForeignKey('auth.User', on_delete=models.CASCADE)
	downloaded_at = models.DateTimeField()
	extraction_script = models.CharField(max_length=250, null=True, blank=True)
	# extraction_script = models.ForeignKey('ExtractionScript', on_delete=models.CASCADE, null=True)
	data_source = models.ForeignKey('DataSource', on_delete=models.CASCADE)
	updated_at = models.DateTimeField(default=timezone.now, null=True, blank=True)
	csv = models.FileField(upload_to=update_filename, null=True)
	zip_file = models.CharField(max_length=100)

	def matched_docs(self):
		return self.datadocument_set.filter(matched = True).count()

	def __str__(self):
		return self.name

	def __unicode__(self):
		return self.title

	def dgurl(self):
		return self.name.replace(' ', '_')

	def get_absolute_url(self):
		return reverse('data_group_edit', kwargs={'pk': self.pk})


@receiver(models.signals.post_delete, sender=DataGroup)
def auto_delete_file_on_delete(sender, instance, **kwargs):
	"""
	Deletes datagroup directory from filesystem
	when datagroup instance is deleted.
	"""
	dg_folder = os.path.split(instance.csv.path)[0]
	if os.path.isdir(dg_folder):
		shutil.rmtree(dg_folder)
