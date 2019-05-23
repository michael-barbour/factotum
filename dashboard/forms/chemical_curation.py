from django import forms

from dashboard.models import DataGroup

class DataGroupSelector(forms.ModelForm):
    document_type = forms.ModelChoiceField(
        queryset=DataGroup.objects.all(),
        label="Data Group",
        required=False)

    class Meta:
        model = DataGroup
        exclude = ( 'id',)

