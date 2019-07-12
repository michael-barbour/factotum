import os
import io
import shutil

from django.test import RequestFactory, TestCase, Client
from django.contrib.auth.models import User
from django.utils.datastructures import MultiValueDict
from django.core.files.uploadedfile import InMemoryUploadedFile, TemporaryUploadedFile

from factotum import settings
from dashboard import views
from dashboard.models import *
from dashboard.tests.loader import fixtures_standard


class RegisterRecordsTest(TestCase):
    fixtures = fixtures_standard

    def setUp(self):
        self.factory = RequestFactory()
        self.client.login(username="Karyn", password="specialP@55word")
        media_root = settings.MEDIA_ROOT
        shutil.rmtree(media_root)

    def tearDown(self):
        # clean up the file system by deleting the data group object
        if DataGroup.objects.filter(name="Walmart MSDS Test Group").exists():
            DataGroup.objects.get(name="Walmart MSDS Test Group").delete()

    def test_datagroup_create(self):
        long_fn = "a filename that is too long " * 10
        csv_string = (
            "filename,title,document_type,url,organization\n"
            "0bf5755e-3a08-4024-9d2f-0ea155a9bd17.pdf,NUTRA NAIL,,, \n"
            f"{long_fn},Body Cream,1,, \n"
        )
        data = io.StringIO(csv_string)
        sample_csv = InMemoryUploadedFile(
            data,
            field_name="csv",
            name="register_records.csv",
            content_type="text/csv",
            size=len(csv_string),
            charset="utf-8",
        )
        form_data = {
            "name": ["Walmart MSDS Test Group"],
            "description": ["test data group"],
            "group_type": ["1"],
            "downloaded_by": [str(User.objects.get(username="Karyn").pk)],
            "downloaded_at": ["08/02/2018"],
            "download_script": ["1"],
            "data_source": ["10"],
        }
        request = self.factory.post(path="/datagroup/new/", data=form_data)
        request.FILES["csv"] = sample_csv
        request.user = User.objects.get(username="Karyn")
        request.session = {}
        request.session["datasource_title"] = "Walmart"
        request.session["datasource_pk"] = 10
        resp = views.data_group_create(request=request, pk=10)
        dg_exists = DataGroup.objects.filter(name="Walmart MSDS Test Group").exists()
        self.assertContains(resp, "Filename too long")
        self.assertFalse(dg_exists)

        csv_string = (
            "filename,title,document_type,url,organization\n"
            "0bf5755e-3a08-4024-9d2f-0ea155a9bd17.pdf,NUTRA NAIL,,, \n"
            "0c68ab16-2065-4d9b-a8f2-e428eb192465.pdf,Body Cream,,, \n"
        )
        data = io.StringIO(csv_string)
        sample_csv = InMemoryUploadedFile(
            data,
            field_name="csv",
            name="register_records.csv",
            content_type="text/csv",
            size=len(csv_string),
            charset="utf-8",
        )
        request = self.factory.post(path="/datagroup/new", data=form_data)
        request.FILES["csv"] = sample_csv
        request.user = User.objects.get(username="Karyn")
        request.session = {}
        request.session["datasource_title"] = "Walmart"
        request.session["datasource_pk"] = 10
        resp = views.data_group_create(request=request, pk=10)

        self.assertEqual(resp.status_code, 302, "Should be redirecting")

        dg = DataGroup.objects.get(name="Walmart MSDS Test Group")

        self.assertEqual(
            f"/datagroup/{dg.pk}/", resp.url, "Should be redirecting to the proper URL"
        )

        # test whether the file system folder was created
        self.assertIn(
            str(dg.fs_id),
            os.listdir(settings.MEDIA_ROOT),
            "The data group's UUID should be a folder in MEDIA_ROOT",
        )

        # In the Data Group Detail Page
        resp = self.client.get(f"/datagroup/{dg.pk}/")

        # test whether the data documents were created
        docs = DataDocument.objects.filter(data_group=dg)
        self.assertEqual(len(docs), 2, "there should be two associated documents")

        # test whether the "Download Registered Records" link is like this example

        # <a href="/datagroup/a9c7f5a7-5ad4-4f75-b877-a3747f0cc081/download_registered_documents" class="btn btn-secondary">
        csv_href = f"/datagroup/{dg.pk}/download_registered_documents/"
        self.assertIn(
            csv_href,
            str(resp._container),
            "The data group detail page must contain the right download link",
        )

        # grab a filename from a data document and see if it's in the csv
        doc_fn = docs.first().filename
        # test whether the registered records csv download link works
        resp_rr_csv = self.client.get(
            csv_href
        )  # this object should be of type StreamingHttpResponse
        docfound = "not found"
        for csv_row in resp_rr_csv.streaming_content:
            if doc_fn in str(csv_row):
                docfound = "found"
        self.assertEqual(
            docfound,
            "found",
            "the document file name should appear in the registered records csv",
        )

        # Test whether the data document csv download works
        # URL on data group detail page: datagroup/docs_csv/{pk}/
        dd_csv_href = (
            f"/datagroup/{dg.pk}/download_documents/"
        )  # this is an interpreted django URL
        resp_dd_csv = self.client.get(dd_csv_href)
        for csv_row in resp_dd_csv.streaming_content:
            if doc_fn in str(csv_row):
                docfound = "found"
        self.assertEqual(
            docfound,
            "found",
            "the document file name should appear in the data documents csv",
        )

        # test whether the "Download All PDF Documents" link works
        dg_zip_href = (
            f"/datagroup/{dg.pk}/download_document_zip/"
        )  # this is the django-interpreted URL
        self.assertIn(
            dg_zip_href,
            str(resp._container),
            "The data group detail page must contain the right zip download link",
        )
        resp_zip = self.client.get(dg_zip_href)

        # test uploading one pdf that matches a registered record
        doc = DataDocument.objects.filter(data_group_id=dg.pk).first()
        pdf = TemporaryUploadedFile(
            name=doc.filename, content_type="application/pdf", size=47, charset=None
        )
        request = self.factory.post(
            path="/datagroup/%s" % dg.pk, data={"upload": "Submit"}
        )
        request.FILES["multifiles"] = pdf
        request.user = User.objects.get(username="Karyn")
        resp = views.data_group_detail(request=request, pk=dg.pk)
        pdf_path = f"{settings.MEDIA_ROOT}{dg.fs_id}/pdf/{doc.get_abstract_filename()}"
        self.assertTrue(
            os.path.exists(pdf_path), "the stored file should be in MEDIA_ROOT/dg.fs_id"
        )
        pdf.close()

    def test_datagroup_create_dupe_filename(self):
        csv_string = (
            "filename,title,document_type,url,organization\n"
            "0bf5755e-3a08-4024-9d2f-0ea155a9bd17.pdf,NUTRA NAIL,1,, \n"
            "0bf5755e-3a08-4024-9d2f-0ea155a9bd17.pdf,Body Cream,1,, \n"
        )
        data = io.StringIO(csv_string)
        sample_csv = InMemoryUploadedFile(
            data,
            field_name="csv",
            name="register_records.csv",
            content_type="text/csv",
            size=len(csv_string),
            charset="utf-8",
        )
        form_data = {
            "name": ["Walmart MSDS Test Group"],
            "description": ["test data group"],
            "group_type": ["1"],
            "downloaded_by": [str(User.objects.get(username="Karyn").pk)],
            "downloaded_at": ["08/02/2018"],
            "download_script": ["1"],
            "data_source": ["10"],
        }
        request = self.factory.post(path="/datagroup/new/", data=form_data)
        request.FILES["csv"] = sample_csv
        request.user = User.objects.get(username="Karyn")
        request.session = {}
        request.session["datasource_title"] = "Walmart"
        request.session["datasource_pk"] = 10
        resp = views.data_group_create(request=request, pk=10)

        self.assertContains(resp, "Duplicate filename found")

    def test_csv_line_endings(self):
        csv_string = (
            "filename,title,document_type,url,organization\r"
            "0bf5755e-3a08-4024-9d2f-0ea155a9bd17.pdf,NUTRA NAIL,,, \r"
            "0c68ab16-2065-4d9b-a8f2-e428eb192465.pdf,Body Cream,,, \r\n"
        )
        data = io.StringIO(csv_string)
        sample_csv = InMemoryUploadedFile(
            data,
            field_name="csv",
            name="register_records.csv",
            content_type="text/csv",
            size=len(csv_string),
            charset="utf-8",
        )
        form_data = {
            "name": ["Walmart MSDS Test Group"],
            "description": ["test data group"],
            "group_type": ["1"],
            "downloaded_by": [f"{User.objects.first().pk}"],
            "downloaded_at": ["08/02/2018"],
            "download_script": ["1"],
            "data_source": ["10"],
        }
        request = self.factory.post(path="/datagroup/new/", data=form_data)
        request.FILES["csv"] = sample_csv
        request.user = User.objects.get(username="Karyn")
        request.session = {"datasource_title": "Walmart", "datasource_pk": 10}
        resp = views.data_group_create(request=request, pk=10)
        dg = DataGroup.objects.filter(name="Walmart MSDS Test Group")
        self.assertTrue(resp.status_code == 302, "Redirect to detail page")
        self.assertTrue(dg.exists(), "Group should be created")
