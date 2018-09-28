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

def create_detail_formset(parent_extext):
# Create the formset factory for the extracted records
    # The model used for the formset depends on whether the 
    # extracted text object matches a data document 
    et = parent_extext
    dd = DataDocument.objects.get(pk=et.pk)
    dg_code = dd.data_group.group_type.code
    if (dg_code == 'FU'):               # Functional use
        detail_model = ExtractedFunctionalUse
        detail_fields = ['extracted_text','raw_cas',
                        'raw_chem_name', 
                        'report_funcuse'
                        ]
    elif (dg_code == 'CO'):              # Composition
        detail_model = ExtractedChemical
        detail_fields = ['extracted_text','raw_cas',
                        'raw_chem_name', 'raw_min_comp',
                        'raw_max_comp', 'unit_type',
                        'report_funcuse',
                        'ingredient_rank',
                        'raw_central_comp']

    elif (dg_code == 'HP' ):             # Habits and practices
        detail_model = ExtractedHabitsAndPractices,
        detail_fields=['product_surveyed',
                        'mass',
                        'mass_unit',
                        'frequency',
                        'frequency_unit',
                        'duration',
                        'duration_unit',
                        'prevalence',
                        'notes']
    
    else:
        detail_model = None
        detail_fields = []
    print('Creating DetailFormsetFactory for group_type %s ' % dg_code)
    print('detail_model: %s ' % detail_model)
    print('fields: %s ' % detail_fields)
    print('detail records: %s' % detail_model.objects.filter(extracted_text = et ).count() )
    DetailFormSet = forms.inlineformset_factory(parent_model=ExtractedText,
                                        model=detail_model,
                                        fields=detail_fields,
                                                extra=1)
    return DetailFormSet(instance=et, prefix='detail')





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

