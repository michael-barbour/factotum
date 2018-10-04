from dal import autocomplete
from django import forms
from dashboard.models import Product, PUC, ProductToPUC, \
                            DataDocument, ExtractedFunctionalUse, \
                            ExtractedChemical, ExtractedText, \
                            ExtractedCPCat, ExtractedHabitsAndPractices, \
                            ExtractedListPresence, ExtractedHabitsAndPracticesToPUC

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
        fields = ['doc_date', 'data_document', 'extraction_script']
        widgets = {
            'data_document': forms.HiddenInput(),
            'extraction_script': forms.HiddenInput(),
        }

def create_detail_formset(parent_exobject):
# Create the formset factory for the extracted records
    # The model used for the formset depends on whether the 
    # extracted text object matches a data document 
    ex = parent_exobject
    ex_model = ex.__class__
    dd = DataDocument.objects.get(pk=ex.pk)
    dg_code = dd.data_group.group_type.code
    
    if (dg_code == 'FU'):               # Functional use
        detail_model = ExtractedFunctionalUse
        detail_fields = ['extracted_text','raw_cas',
                        'raw_chem_name', 
                        'report_funcuse'
                        ]
    elif (dg_code in ['CO','UN']):              # Composition
        detail_model = ExtractedChemical
        detail_fields = ['extracted_text','raw_cas',
                        'raw_chem_name', 'raw_min_comp',
                        'raw_max_comp', 'unit_type',
                        'report_funcuse',
                        'ingredient_rank',
                        'raw_central_comp']

    elif (dg_code == 'HP' ):             # Habits and practices
        detail_model = ExtractedHabitsAndPractices
        detail_fields=['product_surveyed',
                        'mass',
                        'mass_unit',
                        'frequency',
                        'frequency_unit',
                        'duration',
                        'duration_unit',
                        'prevalence',
                        'notes']
    
    elif (dg_code == 'CP' ):             # Chemical Presence List
        ex_model = ExtractedCPCat
        detail_model = ExtractedListPresence
        detail_fields=['extracted_cpcat','raw_cas',
                        'raw_chem_name'
                        ]
    else:
        detail_model = None
        detail_fields = []
    if detail_model != None:
        """         print('Creating DetailFormsetFactory for group_type %s ' % dg_code)
        print('    parent_model: %s ' % ex_model)
        print('    detail_model: %s ' % detail_model)
        print('    fields: %s ' % detail_fields)
        print('    detail record count: %s' % len(list(ex.fetch_extracted_records())) ) """
        detail_factory = forms.inlineformset_factory(parent_model=ex_model,
                                                    model=detail_model,
                                                    fields=detail_fields,
                                                    extra=1)
        extracted_detail_form = detail_factory(instance=ex, prefix='detail')
    else:
        return None
    return extracted_detail_form




# Do not delete these model-specific formset methods.
HnPFormSet = forms.inlineformset_factory(parent_model=ExtractedText,
                                    model=ExtractedHabitsAndPractices,
                                    fields=['product_surveyed',
                                            'mass',
                                            'mass_unit',
                                            'frequency',
                                            'frequency_unit',
                                            'duration',
                                            'duration_unit',
                                            'prevalence',
                                            'notes'],
                                            extra=1)

ChemicalFormSet = forms.inlineformset_factory(parent_model=ExtractedText,
                                    model=ExtractedChemical,
                                    fields=['extracted_text',
                                            'raw_cas',
                                            'raw_chem_name',
                                            'raw_min_comp',
                                            'raw_central_comp',
                                            'raw_max_comp',
                                            'unit_type',
                                            'report_funcuse',
                                            'weight_fraction_type',
                                            'ingredient_rank',
                                            ],
                                    extra=0)

