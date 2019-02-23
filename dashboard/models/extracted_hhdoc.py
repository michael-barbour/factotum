from django.db import models

from .extracted_text import ExtractedText

class ExtractedHHDoc(ExtractedText):
    POPULATION_GENDER = ( 
        ('MALE', 'All-male population'),
        ('FEMALE', 'All-female population'),
        ('BOTH', 'Both male and female population'),
      )
    hhe_report_number = models.CharField("HHE report number", max_length=30,
                                        null=False, blank=False)
    study_location = models.CharField("Study location", max_length=50,
                                        null=True, blank=True)
    naics_code = models.CharField("NAICS code", max_length=10,
                                        null=True, blank=True)
    sampling_date = models.CharField("Date of sampling", max_length=75,
                                        null=True, blank=True)
    population_gender = models.CharField("Gender of population", max_length=75,
                                        choices=POPULATION_GENDER,
                                        null=True, blank=True)
    population_age = models.CharField("Age of population", max_length=75,
                                        null=True, blank=True)
    population_other = models.CharField("Other description of population", max_length=255,
                                        null=True, blank=True)
    occupation = models.CharField("Occupation", max_length=75,
                                        null=True, blank=True)
    facility = models.CharField("Facility", max_length=75,
                                        null=True, blank=True)

    def __str__(self):
        return str(self.hhe_report_number)
    

