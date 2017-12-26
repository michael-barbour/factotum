from django.db import models
from django.utils import timezone
from django.core.urlresolvers import reverse


class Product(models.Model):
	title = models.TextField()
	upc = models.CharField(db_index=True, max_length=40, null=False, blank=False, unique=True)
	url = models.CharField(max_length=255, null=True, blank=True)
	brand_name = models.CharField(db_index=True, max_length=200, null=True, blank=True)
	size = models.CharField(max_length=100, null=True, blank=True)
	color = models.CharField(max_length=100, null=True, blank=True)
	item_id = models.IntegerField(null=True, blank=True)
	parent_item_id = models.IntegerField(null=True, blank=True)
	short_description = models.TextField(null=True, blank=True)
	long_description = models.TextField(null=True, blank=True)
	thumb_image = models.CharField(max_length=255, null=True, blank=True)
	medium_image = models.CharField(max_length=255, null=True, blank=True)
	large_image = models.CharField(max_length=255, null=True, blank=True)
	created_at = models.DateTimeField(default=timezone.now)
	updated_at = models.DateTimeField(null=True, blank=True)

	def __str__(self):
		return self.title

	def __unicode__(self):
		return self.title
