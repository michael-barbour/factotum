from django.db import models
from .common_info import CommonInfo

dgColors = { # ☺☺☺☺☺☺ feel free to make changes here ☺☺☺☺☺☺
        'CO' : '#808000', # Olive
        'HP' : '#469990', # Teal
        'FU' : '#9A6324', # Brown 
        'CP' : '#911eb4', # Purple 
        'HH' : '#e6194b', # Red
        'SU' : '#000075', # Navy
        'UN' : '#2F4F4F', # Slategreyblack
}

class GroupType(CommonInfo):
    title = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    code = models.TextField(null=True, blank=True, max_length=10)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('title',)

    @property
    def color(self):
        return dgColors[self.code]