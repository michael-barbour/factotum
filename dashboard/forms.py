from dal import autocomplete

from django import forms
from django.utils.translation import ugettext_lazy as _

from dashboard.models import *

class ExtractionScriptForm(forms.ModelForm):
    required_css_class = 'required'  # adds to label tag

    class Meta:
        model = Script
        fields = ['title', 'url', 'qa_begun']
        labels = {
            'qa_begun': _('QA has begun'),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(ExtractionScriptForm, self).__init__(*args, **kwargs)



class QANotesForm(forms.ModelForm):

    class Meta:
        model = QANotes
        fields = ['qa_notes']
        widgets = {
            'qa_notes' : forms.Textarea,
        }
        labels = {
            'qa_notes': _('QA Notes (required if approving edited records)'),
        }

class ExtractedTextQAForm(forms.ModelForm):
    required_css_class = 'required'  # adds to label tag

    class Meta:
        model = ExtractedText
        fields = ['prod_name', 'data_document', 'qa_checked']


class BaseExtractedDetailFormSet(forms.BaseInlineFormSet):
    """
    Base class for the form in which users edit the chemical composition or functional use data
    """
    required_css_class = 'required'  # adds to label tag

    class Meta:
        model = ExtractedChemical

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(BaseExtractedDetailFormSet, self).__init__(*args, **kwargs)

        for form in self.forms:
            for field in form.fields:
                form.fields[field].widget.attrs.update(
                                        {'class': 'chem-control form-control'})
#############################################################################
class ProductForm(forms.ModelForm):
    required_css_class = 'required' # adds to label tag
    class Meta:
        model = Product
        fields = ['title', 'manufacturer', 'brand_name', 'upc', 'size', 'color']

class BasePUCForm(forms.ModelForm):
    puc = forms.ModelChoiceField(
        queryset=PUC.objects.all(),
        label='Category',
        widget=autocomplete.ModelSelect2(
            url='puc-autocomplete',
            attrs={'data-minimum-input-length': 3,  })
    )

class ProductPUCForm(BasePUCForm):
    class Meta:
        model = ProductToPUC
        fields = ['puc']

class HabitsPUCForm(BasePUCForm):
    class Meta:
        model = ExtractedHabitsAndPracticesToPUC
        fields = ['puc']

class ExtractedTextForm(forms.ModelForm):

    class Meta:
        model = ExtractedText
        fields = ['prod_name', 'doc_date', 'rev_num']

class ExtractedTextForm(forms.ModelForm):
    class Meta:
        model = ExtractedText
        fields = ['prod_name', 'rev_num', 'doc_date']

        widgets = {
            'data_document': forms.HiddenInput(),
            'extraction_script': forms.HiddenInput(),
        }

class ExtractedCPCatForm(ExtractedTextForm):
    class Meta:
        model = ExtractedCPCat
        fields = ['doc_date', 'data_document', 'extraction_script', 'cat_code', 'description_cpcat','cpcat_sourcetype']

class DocumentTypeForm(forms.ModelForm):
    class Meta:
        model = DataDocument
        fields = ['document_type']

    def __init__(self, *args, **kwargs):
        super(DocumentTypeForm, self).__init__(*args, **kwargs)
        self.fields['document_type'].label = ''
        self.fields['document_type'].widget.attrs.update({
            'onchange': 'form.submit();'
        })


def create_detail_formset(group_type):
    '''Returns the pair of formsets that will be needed based on group_type.
    '''
    def one(): # for chemicals
        detail_fields = ['extracted_text','raw_cas','raw_chem_name',
                        'raw_min_comp','raw_max_comp', 'unit_type',
                        'report_funcuse','ingredient_rank','raw_central_comp']
        ChemicalFormSet = forms.inlineformset_factory(parent_model=ExtractedText,
                                                model=ExtractedChemical,
                                                fields=detail_fields,
                                                extra=1)
        return (ExtractedTextForm, ChemicalFormSet)

    def two(): # for functional_use
        detail_fields = ['extracted_text','raw_cas',
                            'raw_chem_name','report_funcuse']
        FunctionalUseFormSet = forms.inlineformset_factory(parent_model=ExtractedText,
                                                model=ExtractedFunctionalUse,
                                                fields=detail_fields,
                                                extra=1)
        return (ExtractedTextForm, FunctionalUseFormSet)

    def three(): # for habits_and_practices
        detail_fields = ['product_surveyed','mass','mass_unit','frequency',
                        'frequency_unit','duration','duration_unit',
                        'prevalence','notes']
        HnPFormSet = forms.inlineformset_factory(parent_model=ExtractedText,
                                                model=ExtractedHabitsAndPractices,
                                                fields=detail_fields,
                                                extra=1)
        return (ExtractedTextForm, HnPFormSet)

    def four(): # for extracted_list_presence
        detail_fields = ['extracted_cpcat','raw_cas','raw_chem_name']
        ListPresenceFormSet = forms.inlineformset_factory(parent_model=ExtractedCPCat,
                                                model=ExtractedListPresence,
                                                fields=detail_fields,
                                                extra=1)
        return (ExtractedCPCatForm, ListPresenceFormSet)
    dg_types = {
        'CO': one,
        'UN': one,
        'FU': two,
        'HP': three,
        'CP': four,
    }
    func = dg_types.get(group_type, lambda: None)
    return func()

# # Do not delete these model-specific formset methods.
# HnPFormSet = forms.inlineformset_factory(parent_model=ExtractedText,
#                                     model=ExtractedHabitsAndPractices,
#                                     fields=['product_surveyed',
#                                             'mass',
#                                             'mass_unit',
#                                             'frequency',
#                                             'frequency_unit',
#                                             'duration',
#                                             'duration_unit',
#                                             'prevalence',
#                                             'notes'],
#                                             extra=1)
#
# ChemicalFormSet = forms.inlineformset_factory(parent_model=ExtractedText,
#                                     model=ExtractedChemical,
#                                     fields=['extracted_text',
#                                             'raw_cas',
#                                             'raw_chem_name',
#                                             'raw_min_comp',
#                                             'raw_central_comp',
#                                             'raw_max_comp',
#                                             'unit_type',
#                                             'report_funcuse',
#                                             'weight_fraction_type',
#                                             'ingredient_rank',
#                                             ],
#                                     extra=0)
