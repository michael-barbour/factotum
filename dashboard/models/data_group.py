import os

from django.db import models
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.dispatch import receiver

class DataGroup(models.Model):

	name = models.CharField(max_length=50)
	description = models.TextField(null=True, blank=True)
	downloaded_by = models.ForeignKey('auth.User', on_delete=models.CASCADE)
	downloaded_at = models.DateTimeField()
	extraction_script = models.CharField(max_length=250, null=True, blank=True)
	data_source = models.ForeignKey('DataSource', on_delete=models.CASCADE)
	updated_at = models.DateTimeField(default=timezone.now, null=True, blank=True)
	csv = models.FileField(upload_to='csv/')

	def __str__(self):
		return self.name

	def __unicode__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('data_group_edit', kwargs={'pk': self.pk})

# @login_required()
# def register_upload(request, template='data_document/upload.html'):
#     datagroup_pk = request.session['datagroup_pk']
#     datagroup = DataGroup.objects.filter(pk=datagroup_pk)[0]
#     context = {'datagroup_pk': datagroup_pk,}
#     if request.method == 'POST' and request.FILES['myfile']:
#         user = request.user.username + '_'
#         myfile = request.FILES['myfile']
#         fs = FileSystemStorage()
#         fn = './{}/{}'.format(datagroup, myfile.name)
#         filename = fs.save(fn, myfile)
#         uploaded_file_url = fs.url(filename)
#         context['uploaded_file_url'] = uploaded_file_url
#         print(os.path.join(os.getcwd(), uploaded_file_url))
#         print(os.getcwd())
#         with open(uploaded_file_url) as csvfile:
#             reader = csv.DictReader(csvfile)
#             up_num = len([i for i,d in enumerate(reader) if d['filename']])
#             valid = up_num == reader.line_num-1
#         if not valid: # missing filenames, delete and prompt to fix
#             context['uploaded_file_url'] = 0
#             context['fail'] = (reader.line_num-1) -up_num
#             fs.delete(os.path.join(os.getcwd(), uploaded_file_url)) # problems here, test
#             return render(request, template, context)
#         # if not DataDocument.objects.last():
#         #     start = 0
#         # else:
#         #     start = DataDocument.objects.last().pk
#         new_f = '/'.join(uploaded_file_url.split('/')[:-1]+[user + myfile.name])
#         ordered_fieldnames = OrderedDict([('DataDocument_id',None),
#                                             ('filename',None),
#                                             ('title',None),
#                                             ('product',None),
#                                             ('url',None)])
#         with open(uploaded_file_url, 'r') as csvfile:
#             reader = csv.DictReader(csvfile)
#             with open(new_f, 'w') as f:
#                 writer = csv.DictWriter(f, fieldnames=ordered_fieldnames,
#                                         lineterminator='\n')
#                 writer.writeheader()
#                 for row in reader:
#                     print(row['filename'])
#                     if not row['title']:
#                         row['title'] = row['filename'].split('.')[0]
#                     doc = DataDocument(filename=row['filename'],
#                                         title=row['title'],
#                                         url=row['url'],
#                                         product_category=row['product'],
#                                         data_group=datagroup)
#                     doc.save()
#                     row['DataDocument_id'] = doc.id
#                     writer.writerow(row)
#         fs.delete(os.path.join(os.getcwd(), uploaded_file_url))
#         context['uploaded_num'] = up_num


@receiver(models.signals.post_delete, sender=DataGroup)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `csv` object is deleted.
    """
    if instance.csv:
        if os.path.isfile(instance.csv.path):
            os.remove(instance.csv.path)
