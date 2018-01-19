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

	def get_data_document_count(self):
		return self.datadocument_set.filter().count()

	def get_pct_checked(self):
		return 0.5

class ExtractionScriptManager(models.Manager):
    def with_docs_checked(self):
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT s.*, COUNT(*)
                FROM dashboard_datadocument dd , dashboard_extractionscript s
                WHERE s.id = dd.poll_id
                GROUP BY s.*
                ORDER BY s.poll_date DESC""")
            result_list = []
            for row in cursor.fetchall():
                p = self.model(id=row[0], question=row[1], poll_date=row[2])
                p.num_responses = row[3]
                result_list.append(p)
        return result_list