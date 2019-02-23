from dal import autocomplete
from bootstrap_datepicker_plus import DatePickerInput

from django import forms
from django.forms import BaseInlineFormSet

from django.utils.translation import ugettext_lazy as _

from dashboard.models import *
from django.db.models import F
from dashboard.utils import get_extracted_models

class DataGroupForm(forms.ModelForm):
    required_css_class = 'required' # adds to label tag

    class Meta:
        model = DataGroup
        fields = ['name','description','url','group_type','downloaded_by',
                    'downloaded_at','download_script','data_source','csv']
        widgets = {'downloaded_at': DatePickerInput()}
        labels = {'csv': _('Register Records CSV File'),
                  'url': _('URL'), }

    def __init__(self, *args, **kwargs):
        qs = Script.objects.filter(script_type='DL')
        self.user = kwargs.pop('user', None)
        super(DataGroupForm, self).__init__(*args, **kwargs)
        self.fields['csv'].widget.attrs.update({'accept':'.csv'})
        self.fields['download_script'].queryset = qs

class ExtractionScriptForm(forms.Form):
    required_css_class = 'required' # adds to label tag
    script_selection = forms.ModelChoiceField(
                            queryset=Script.objects.filter(script_type='EX'),
                            label="Extraction Script")
    weight_fraction_type = forms.ModelChoiceField(
                            queryset=WeightFractionType.objects.all(),
                            label="Weight Fraction Type",
                            initial="1")
    extract_file = forms.FileField(label="Extracted Text CSV File")

    def __init__(self, *args, **kwargs):
        self.dg_type = kwargs.pop('dg_type', 0)
        self.user = kwargs.pop('user', None)
        super(ExtractionScriptForm, self).__init__(*args, **kwargs)
        self.fields['weight_fraction_type'].widget.attrs.update(
                                        {'style':'height:2.75rem; !important'})
        self.fields['script_selection'].widget.attrs.update(
                                        {'style':'height:2.75rem; !important'})
        self.fields['extract_file'].widget.attrs.update({'accept':'.csv'})
        if self.dg_type in ['FU','CP']:
            del self.fields['weight_fraction_type']
        self.collapsed = True

class CleanCompDataForm(forms.Form):
    required_css_class = 'required' # adds to label tag
    script_selection = forms.ModelChoiceField(
                            queryset=Script.objects.filter(script_type='DC'),
                            label="Data Cleaning Script",
                            required=True)
    clean_comp_data_file = forms.FileField(label="Clean Composition Data CSV File",
                            required=True)

    def __init__(self, *args, **kwargs):
        super(CleanCompDataForm, self).__init__(*args, **kwargs)
        self.fields['script_selection'].widget.attrs.update(
                                        {'style':'height:2.75rem; !important'})
        self.fields['clean_comp_data_file'].widget.attrs.update({'accept':'.csv'})
        self.collapsed = True

class DataSourceForm(forms.ModelForm):
    required_css_class = 'required'
    class Meta:
        model = DataSource
        fields = ['title', 'url', 'estimated_records', 'state', 'priority',
                  'description']

class PriorityForm(forms.ModelForm):
    class Meta:
        model = DataSource
        fields = ['priority']

    def __init__(self, *args, **kwargs):
        super(PriorityForm, self).__init__(*args, **kwargs)
        self.fields['priority'].label = ''
        self.fields['priority'].widget.attrs.update({
            'onchange': 'form.submit();'
            })

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


class ProductLinkForm(forms.ModelForm):
    required_css_class = 'required' # adds to label tag
    document_type = forms.ModelChoiceField(
        queryset=DocumentType.objects.all(),
        label="Data Document Type",
        required=True)
    return_url = forms.CharField()

    class Meta:
        model = Product
        fields = ['title', 'manufacturer', 'brand_name', 'upc', 'size', 'color']

    def __init__(self, *args, **kwargs):
        super(ProductLinkForm, self).__init__(*args, **kwargs)
        self.fields['return_url'].widget = forms.HiddenInput()

class ProductForm(forms.ModelForm):
    required_css_class = 'required' # adds to label tag

    class Meta:
        model = Product
        fields = ['title','manufacturer','brand_name','size','color',
                    'model_number','short_description','long_description']

class ProductViewForm(ProductForm):
    class Meta(ProductForm.Meta):
        exclude = ('title', 'long_description',)

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        for f in self.fields:
            self.fields[f].disabled = True

class BasePUCForm(forms.ModelForm):
    puc = forms.ModelChoiceField(
        queryset=PUC.objects.all(),
        label='Category',
        widget=autocomplete.ModelSelect2(
            url='puc-autocomplete',
            attrs={'data-minimum-input-length': 3,})
    )

class ProductPUCForm(BasePUCForm):
    class Meta:
        model = ProductToPUC
        fields = ['puc']

class HabitsPUCForm(BasePUCForm):
    class Meta:
        model = ExtractedHabitsAndPracticesToPUC
        fields = ['puc']

class BulkProductPUCForm(forms.ModelForm):
    id_pks = forms.CharField(label='Product Titles',
                             widget=forms.HiddenInput(),
                             required=True)
    class Meta:
        model = ProductToPUC
        fields = ['puc', 'id_pks']

class BulkProductTagForm(BasePUCForm):
    required_css_class = 'required' # adds to label tag
    tag = forms.ModelChoiceField(queryset=PUCTag.objects.none(),
                                 label='Attribute')
    id_pks = forms.CharField(label='Product Titles',
                             widget=forms.HiddenInput())
    class Meta:
        model = ProductToPUC
        fields = ['puc', 'tag', 'id_pks']
    def __init__(self, *args, **kwargs):
        super(BulkProductTagForm, self).__init__(*args, **kwargs)
        self.fields['puc'].label = 'Select PUC for Attribute to Assign to Selected Products'
        self.fields['tag'].label = 'Select Attribute to Assign to Selected Products'
        self.fields['puc'].widget.attrs['onchange'] = 'form.submit();'

class ExtractedTextForm(forms.ModelForm):
    class Meta:
        model = ExtractedText
        fields = ['prod_name', 'rev_num', 'doc_date','extraction_script']

        widgets = {
            'data_document': forms.HiddenInput(),
            #'extraction_script': forms.HiddenInput(),
        }

class ExtractedCPCatForm(ExtractedTextForm):
    class Meta:
        model = ExtractedCPCat
        exclude=['data_document']


class ExtractedHHDocForm(ExtractedTextForm):
    class Meta:
        model = ExtractedHHDoc
        exclude=['data_document']

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

def include_extract_form(dg):
    '''Returns the ExtractionScriptForm based on conditions of DataGroup
    type as well as whether all records are matched, but not extracted
    '''
    if not dg.type in ['FU','CO','CP']:
        return False
    if dg.all_matched() and not dg.all_extracted():
        return ExtractionScriptForm(dg_type=dg.type)
    else:
        return False

class ExtractedChemicalFormSet(BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class ExtractedChemicalForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ExtractedChemicalForm, self).__init__(*args, **kwargs)
        # the subclass properties need to be explicitly added
        for subclassfield in type(self.instance)._meta.get_fields():
            # but we are overriding the exclude list, so re-exclude them
            if not subclassfield.name in self._meta.exclude:
                # Add each field, determining the type as best as possible
                if subclassfield.is_relation:           # relation fields use ModelChoiceField widgets
                                                        # for editable input forms, links for others?
                    self.fields[subclassfield.name] = forms.ModelChoiceField(
                        # queryset=subclassfield.model.objects.filter(id=subclassfield.value_from_object(self.instance)),
                        queryset=subclassfield.remote_field.model.objects.all(),
                        label=subclassfield.verbose_name
                        )
                elif subclassfield.get_internal_type() in ['PositiveIntegerField','BigIntegerField']:
                    self.fields[subclassfield.name] = forms.IntegerField(label=subclassfield.verbose_name)
                elif subclassfield.get_internal_type() in ['DecimalField','FloatField']:
                    self.fields[subclassfield.name] = forms.DecimalField(label=subclassfield.verbose_name)
                elif subclassfield.get_internal_type() in ['DateField','DateTimeField']:
                    self.fields[subclassfield.name] = forms.DateTimeField( label=subclassfield.verbose_name)
                else:   
                    self.fields[subclassfield.name] = forms.CharField(max_length=200, label=subclassfield.verbose_name)
                
                self.fields[subclassfield.name].initial = subclassfield.value_from_object(self.instance)
        # For curated chemicals, add each of the related properties from DSSToxLookup 
        if hasattr(self.instance, 'dsstox') and self.instance.dsstox is not None:
            for curatedfield in type(self.instance.dsstox)._meta.get_fields():
                if curatedfield.name in ['sid','true_chemname','true_cas']:
                    self.fields[curatedfield.name] = forms.CharField(
                        max_length=200, 
                        label = curatedfield.verbose_name
                        )
                    self.fields[curatedfield.name].initial = curatedfield.value_from_object(self.instance.dsstox)
                    self.fields[curatedfield.name].widget.attrs.update({'class' : 'curated'})

    class Meta:
        model = RawChem
        exclude = ('data_document','created_at','updated_at','dsstox','id')

def include_clean_comp_data_form(dg):
    '''Returns the CleanCompDataForm based on conditions of DataGroup
    type = Composition and at least 1 document extracted
    '''
    if not dg.type in ['CO']:
        return False
    if dg.extracted_docs() > 0:
        return CleanCompDataForm()
    else:
        return False




def create_detail_formset(group_type, extra=1, can_delete=False):
    '''Returns the pair of formsets that will be needed based on group_type.
    .                       ('CO'),('CP'),('FU'),('HP'),('HH')
    .

    '''
    parent, child = get_extracted_models(group_type)
    def make_formset(parent_model,model,fields):
        return forms.inlineformset_factory(parent_model=parent_model,
                                            model=model,
                                            fields=fields,
                                            extra=extra,
                                            can_delete=False)

    def make_custom_formset(parent_model,model,fields,formset,form):
        return forms.inlineformset_factory(parent_model=parent_model,
                                            model=model,
                                            fields=fields,
                                            formset=formset, #this specifies a custom formset
                                            form=form,
                                            extra=extra,
                                            can_delete=False)

    def one(): # for chemicals or unknown
        ChemicalFormSet = make_custom_formset(
            parent_model=parent,
            model=child,
            fields=child.detail_fields(),
            formset=ExtractedChemicalFormSet,
            form=ExtractedChemicalForm
            )
        return (ExtractedTextForm, ChemicalFormSet)

    def two(): # for functional_use
        FunctionalUseFormSet = make_formset(parent,child,child.detail_fields())
        return (ExtractedTextForm, FunctionalUseFormSet)

    def three(): # for habits_and_practices
        HnPFormSet = make_formset(parent,child,child.detail_fields())
        return (ExtractedTextForm, HnPFormSet)

    def four(): # for extracted_list_presence
        ListPresenceFormSet = make_custom_formset(
            parent_model=parent,
            model=child,
            fields=child.detail_fields(),
            formset=ExtractedChemicalFormSet,
            form=ExtractedChemicalForm
            )
        return (ExtractedCPCatForm, ListPresenceFormSet)

    def five(): # for extracted_hh_rec
        #HHFormSet = make_formset(parent,child,child.detail_fields())
        HHFormSet = make_custom_formset(
        parent_model=parent,
        model=child,
        fields=child.detail_fields(),
        formset=ExtractedChemicalFormSet,
        form=ExtractedChemicalForm
        )
        return (ExtractedHHDocForm, HHFormSet)

    dg_types = {
        'CO': one,
        'UN': one,
        'FU': two,
        'HP': three,
        'CP': four,
        'HH': five,
    }
    func = dg_types.get(group_type, lambda: None)
    return func()
