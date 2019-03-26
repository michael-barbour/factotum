from django.contrib.auth.decorators import login_required
from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from dashboard.models import *
import datetime
import csv


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


@login_required()
def upload_raw_chem_csv(request):
    data = {}
    if "GET" == request.method:
        return render(request, "chemical_curation/chemical_curation_index.html", data)
        # if not GET, then proceed
    try:
        csv_file = request.FILES["csv_file"]
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'File is not CSV type')
            return HttpResponseRedirect(reverse("upload_raw_chem_csv"))
        # if file is too large, return
        if csv_file.multiple_chunks():
            messages.error(request, "Uploaded file is too big (%.2f MB)." % (csv_file.size / (1000 * 1000),))
            return HttpResponseRedirect(reverse("upload_raw_chem_csv"))
        # TODO if file does not have the right column headers, return

        file_data = csv_file.read().decode("utf-8")

        lines = file_data.split("\n")
        # loop over the lines and save them in db. If error , store as string and then display
        for line in lines:
            fields = line.split(",")
            data_dict = {}
            data_dict["name"] = fields[0]
            data_dict["start_date_time"] = fields[1]
            data_dict["end_date_time"] = fields[2]
            data_dict["notes"] = fields[3]
        try:
            form = EventsForm(data_dict)
            if form.is_valid():
                form.save()
        except Exception as e:
            pass

    except Exception as e:
        messages.error(request, "Unable to upload file. " + repr(e))

    return HttpResponseRedirect(reverse("upload_raw_chem_csv"))
