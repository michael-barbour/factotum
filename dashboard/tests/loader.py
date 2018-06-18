from django.utils import timezone
from django.contrib.auth.models import User

from dashboard.models import (SourceType, DataSource, DataGroup, DataDocument,
                              Script, ExtractedText, ExtractedChemical,
                              ExtractedFunctionalUse, Product, PUC)

class dotdict(dict):
    """dot.notation access to dictionary attributes"""
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

def load_model_objects():
    user = User.objects.create_user(username='Karyn',
                                        password='specialP@55word')
    st = SourceType.objects.create(title='msds/sds')
    ds = DataSource.objects.create(title='Data Source for Test',
                                        estimated_records=2, state='AT',
                                        priority='HI', type=st)
    script = Script.objects.create(title='Test Title',
                                        url='http://www.epa.gov/',
                                        qa_begun=False, script_type='DL')
    dg = DataGroup.objects.create(name='Data Group for Test',
                                        description='Testing...',
                                        data_source = ds,
                                        download_script=script,
                                        downloaded_by=user,
                                        downloaded_at=timezone.now(),
                                        csv='register_records_matching.csv')
    doc = DataDocument.objects.create(title='test document',
                                            data_group=dg,
                                            source_type=st)

    p = Product.objects.create(data_source=ds,
                                upc='Test UPC for ProductToPUC')

    puc = PUC.objects.create(gen_cat='Test General Category',
                              prod_fam='Test Product Family',
                              prod_type='Test Product Type')

    extext = ExtractedText.objects.create(
                                    prod_name='Test Extracted Text Record',
                                    data_document=doc,
                                    extraction_script=script
                                    )

    return dotdict({'user':user,
                    'st':st,
                    'ds':ds,
                    'script':script,
                    'dg':dg,
                    'doc':doc,
                    'p':p,
                    'puc':puc,
                    'extext':extext,
                    })
