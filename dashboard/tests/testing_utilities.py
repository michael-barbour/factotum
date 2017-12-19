import json
from selenium import webdriver
from django.test import TestCase, RequestFactory
from dashboard.models import DataSource
from dashboard.models import SourceType
from dashboard.models import DataGroup
from django.contrib.auth.models import User
from django.utils import timezone
from django.test import Client

def populate_test_db():
    """
    Adds records to an empty test database
    """
    User.objects.create_superuser(
        username='admin',
        email='admin@test.com',
        password='t0ps3cret')

    SourceType.objects.create(title='Test SourceType')

    DataSource.objects.create(
        title='Test Data Source', 
        url="test_url.com", 
        estimated_records=100,
        type=SourceType.objects.get(title='Test SourceType'),
        state='AT',
        description='a description of the data source',
        created_at='2017-12-18 20:09:49'
        )
    
    DataGroup.objects.create(
        name = 'Test DG 1',
        description = 'A test Data Group object',
        downloaded_by = User.objects.get(username='admin'),
        downloaded_at = '2017-12-18 22:09:49',
        extraction_script = 'script_name.rmd',
        data_source = DataSource.objects.get(pk=1),
        csv = '',
        zip_file = ''
    )
    
