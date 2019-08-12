from six import text_type
from taggit.models import TaggedItemBase, TagBase
from taggit.managers import TaggableManager

from django.db import models
from django.utils.translation import ugettext_lazy as _

from .raw_chem import RawChem
from .common_info import CommonInfo


class ExtractedListPresence(CommonInfo, RawChem):

    qa_flag = models.BooleanField(default=False)
    report_funcuse = models.CharField(
        "Reported functional use", max_length=100, null=True, blank=True
    )
    tags = TaggableManager(
        through="dashboard.ExtractedListPresenceToTag",
        to="dashboard.ExtractedListPresenceTag",
        blank=True,
    )

    @classmethod
    def detail_fields(cls):
        return ["raw_cas", "raw_chem_name", "report_funcuse"]

    def __str__(self):
        return str(self.raw_chem_name) if self.raw_chem_name else ""

    def get_datadocument_url(self):
        return self.extracted_text.data_document.get_absolute_url()

    def get_extractedtext(self):
        return self.extracted_text

    @property
    def data_document(self):
        return self.extracted_text.data_document

    def __get_label(self, field):
        return text_type(self._meta.get_field(field).verbose_name)

    @property
    def report_funcuse_label(self):
        return self.__get_label("report_funcuse")


class ExtractedListPresenceToTag(TaggedItemBase, CommonInfo):
    content_object = models.ForeignKey(ExtractedListPresence, on_delete=models.CASCADE)
    tag = models.ForeignKey(
        "ExtractedListPresenceTag",
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_items",
    )

    class Meta:
        verbose_name = _("Extracted list presence to keyword")
        verbose_name_plural = _("Extracted list presence to keywords")
        ordering = ("content_object",)

    def __str__(self):
        return str(self.content_object)


class ExtractedListPresenceTag(TagBase, CommonInfo):

    KIND_CHOICES = [
        ("GU", "General use"),
        ("PH", "Pharmaceutical"),
        ("LP", "List presence"),
    ]

    definition = models.CharField("Definition", max_length=750, null=True, blank=True)
    kind = models.CharField(max_length=2, default="GU", choices=KIND_CHOICES)

    class Meta:

        verbose_name = _("Extracted list presence keyword")
        verbose_name_plural = _("Extracted list presence keywords")
        ordering = ("name",)

    def __str__(self):
        return self.name
