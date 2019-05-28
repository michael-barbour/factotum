from django.contrib.auth.decorators import login_required
from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect, HttpResponse, StreamingHttpResponse
from django.contrib import messages
from dashboard.models import *
from django import forms
from dashboard.forms import DataGroupSelector
import datetime
import csv
from django.db.models import Value, IntegerField



@login_required()
def chemical_curation_index(request, template_name='chemical_curation/chemical_curation_index.html'):
    uncurated_chemical_count = RawChem.objects.filter(dsstox_id=None).count()
    records_processed = 0

    dg_picker_form = DataGroupSelector()

    data = {'dg_picker_form': dg_picker_form, 'uncurated_chemical_count':
            uncurated_chemical_count, 'records_processed': records_processed}
    # if not GET, then proceed
    if "POST" == request.method:
        try:
            # if not a csv file
            csv_file = request.FILES["csv_file"]
            if not csv_file.name.endswith('.csv'):
                data.update({'error_message': 'File is not CSV type'})
                return render(request, template_name, data)
            # if file is too large, return
            if csv_file.multiple_chunks():
                error = "Uploaded file is too big (%.2f MB)." % (
                    csv_file.size / (1000 * 1000))
                data.update({'error_message': error})
                return render(request, template_name, data)

            file_data = csv_file.read().decode("utf-8")
            lines = file_data.split("\n")

            # loop over the lines and save them in db. If error , store as string and then display
            records_processed = len(lines) - 1
            for line in lines:
                fields = line.split(",")
                data_dict = {}
                data_dict["raw_chemical_id"] = fields[0].strip()
                data_dict["rid"] = fields[1].strip()
                data_dict["sid"] = fields[2].strip()
                data_dict["true_chemical_name"] = fields[3].strip()
                data_dict["true_cas"] = fields[4].strip()
                # If it is the header row check to see that the columns are in order.
                if data_dict["raw_chemical_id"] == "external_id":
                    if (data_dict["raw_chemical_id"] != "external_id") or (data_dict['sid'] != 'sid') or \
                            (data_dict['true_chemical_name'] != "true_chemical_name") or \
                            (data_dict['true_cas'] != 'true_cas'):
                        data.update(
                            {"error_message": "Check to ensure your column headers are in order."})
                        return render(request, template_name, data)
                else:
                    try:
                        # Check to see of SID exists,
                        if DSSToxLookup.objects.filter(sid=data_dict['sid']).exists():
                            # if is does exist Overwrite the existing True CAS and Chemname
                            DSSToxLookup.objects.filter(sid=data_dict['sid']). \
                                update(true_cas=data_dict["true_cas"],
                                       true_chemname=data_dict["true_chemical_name"])
                        # if not create it in DSSToxLookup
                        else:
                            chem = DSSToxLookup.objects.create(true_cas=data_dict["true_cas"],
                                                               true_chemname=data_dict["true_chemical_name"],
                                                               sid=data_dict["sid"])
                            chem.save()
                        # ensure link back to DSSToxLookup
                        sid_id = DSSToxLookup.objects.filter(
                            sid=data_dict['sid'])
                        RawChem.objects.filter(id=data_dict["raw_chemical_id"]).update(rid=data_dict['rid'],
                                                                                       dsstox_id=sid_id[0].id)
                    except Exception as e:
                        print(e)
                        pass

        except Exception as e:
            # This is the catchall - MySQL database has went away, etc....
            error = "Something is seriously wrong with this csv - %s" % repr(e)
            data.update({"error_messasage": error})
            return render(request, template_name, data)
            messages.error(request, "Unable to upload file. " + repr(e))
    if records_processed > 0:
        data.update({"records_processed": records_processed})
    return render(request, template_name, data)


@login_required()
def download_raw_chems(stats):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="uncurated_chemicals_%s.csv"' % \
                                      (datetime.datetime.now().strftime("%Y%m%d"))

    writer = csv.writer(response)
    writer.writerow(['dashboard_rawchem_id', 'raw_cas',
                     'raw_chem_name', 'rid', 'datagroup_id'])
    for rc in RawChem.objects.filter(dsstox_id=None):
        writer.writerow([rc.id, rc.raw_cas, rc.raw_chem_name,
                         rc.rid if rc.rid else '', rc.data_group_id])
    return response

# This clever way to combine writing the headers
# with writing the rows, including the "yield" keyword, is from
# https://stackoverflow.com/questions/45578196/adding-rows-manually-to-streaminghttpresponse-django

class Echo:
    """An object that implements just the write method of the file-like
    interface.
    """

    def write(self, value):
        """Write the value by returning it, instead of storing in a buffer."""
        return value

def iterate_rawchems(rows, pseudo_buffer):
    writer = csv.writer(pseudo_buffer)
    yield pseudo_buffer.write("id, raw_cas,raw_chem_name, rid, datagroup_id\n")
    for row in rows:
        yield writer.writerow([row['id'], row['raw_cas'], row['raw_chem_name'],
        row['rid']  if row['rid'] else '',
                         row['dg_id']])

@login_required()
def download_raw_chems_dg(request, pk):
    dg = DataGroup.objects.get(pk=pk)

    # Limit the response to 10,000 records
    uncurated_chems = RawChem.objects.filter(dsstox_id=None).filter(extracted_text__data_document__data_group=dg).annotate(dg_id = Value(pk, IntegerField())).values('id', 'raw_cas', 'raw_chem_name', 'rid', 'dg_id')[0:10000]
    pseudo_buffer = Echo()
    writer = csv.writer(pseudo_buffer)
    response = StreamingHttpResponse(
        streaming_content=(iterate_rawchems(uncurated_chems, pseudo_buffer)),
        content_type='text/csv'
    )
    
    response['Content-Disposition'] = 'attachment; filename="uncurated_chemicals_%s_%s.csv"' % \
                                      (pk, datetime.datetime.now().strftime("%Y%m%d"))
    return response
