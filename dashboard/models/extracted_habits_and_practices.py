from django.db import models
from .common_info import CommonInfo
from django.core.exceptions import ValidationError
from .extracted_text import ExtractedText


class ExtractedHabitsAndPractices(CommonInfo):
    extracted_text = models.ForeignKey(
        ExtractedText, on_delete=models.CASCADE, related_name="practices"
    )
    product_surveyed = models.CharField("Product Surveyed", max_length=50)
    PUCs = models.ManyToManyField(
        "dashboard.PUC", through="dashboard.ExtractedHabitsAndPracticesToPUC"
    )
    mass = models.DecimalField(
        "Mass", max_digits=12, decimal_places=5, null=True, blank=True
    )
    mass_unit = models.CharField("Units for Mass", max_length=40, blank=True)
    frequency = models.DecimalField(
        "Frequency", max_digits=12, decimal_places=5, null=True, blank=True
    )
    frequency_unit = models.CharField("Units for Frequency", max_length=40, blank=True)
    duration = models.DecimalField(
        "Duration", max_digits=12, decimal_places=5, null=True, blank=True
    )
    duration_unit = models.CharField("Units for Duration", max_length=40, blank=True)
    prevalence = models.CharField("Prevalence", max_length=200, blank=True)
    notes = models.TextField("Notes", blank=True)

    def __str__(self):
        return self.product_surveyed

    @classmethod
    def detail_fields(cls):
        return [
            "product_surveyed",
            "mass",
            "mass_unit",
            "frequency",
            "frequency_unit",
            "duration",
            "duration_unit",
            "prevalence",
            "notes",
        ]

    def clean(self):
        if self.mass and self.mass_unit == "":
            msg = "Mass unit must be supplied if mass is specified."
            raise ValidationError({"mass_unit": msg})
        if self.frequency and self.frequency_unit == "":
            msg = "Frequency unit must be supplied if frequency is specified."
            raise ValidationError({"frequency_unit": msg})
        if self.duration and self.duration_unit == "":
            msg = "Duration unit must be supplied if duration is specified."
            raise ValidationError({"duration_unit": msg})

    def get_extractedtext(self):
        return self.extracted_text

    @property
    def data_document(self):
        return self.extracted_text.data_document
