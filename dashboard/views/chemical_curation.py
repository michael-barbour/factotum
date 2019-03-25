from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from dashboard.models import *


@login_required()
def chemical_curation_index(request, template_name='chemical_curation/chemical_curation_index.html'):
    uncurated_chemical_count = RawChem.objects.filter(dsstox_id=None).count()
    data = {'uncurated_chemical_count': uncurated_chemical_count}
    return render(request, template_name, data)


@login_required()
def download_raw_chems(stats):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="uncurated_chemicals_%s.csv"' % \
                                      (datetime.datetime.now().strftime("%Y%m%d"))

    writer = csv.writer(response)
    writer.writerow(['dashboard_rawchem_id', 'raw_cas', 'raw_chem_name', 'rid'])
    for rawchem in RawChem.objects.filter(dsstox_id=None):
        writer.writerow([rawchem.id, rawchem.raw_cas, rawchem.raw_chem_name, rawchem.rid if rawchem.rid else ''])
    return response
