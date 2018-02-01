Reference URLS:

http://django-haystack.readthedocs.io/en/master/tutorial.html#installation

https://github.com/nazariyg/Solr-5-for-django-haystack

`brew install solr`

`ls /usr/local/Cellar/solr/7.2.0/server/solr`

`sudo su - solr -c '/opt/solr/bin/solr create -c factotum -d basic_configs'`

`pip install pysolr`

`pip install django-haystack`

installs version 2.6.1

Add `include` to dashboard/urls.py:

`from django.conf.urls import url, include`

Add the route:
`    url(r'^search/', include('haystack.urls')),`

Add the `search/search.html` template from 

The solr schema needs to be specified:
https://lucene.apache.org/solr/guide/6_6/schema-factory-definition-in-solrconfig.html#SchemaFactoryDefinitioninSolrConfig-SwitchingfromManagedSchematoManuallyEditedschema.xml



`python manage.py build_solr_schema --filename=/usr/local/Cellar/solr/7.2.0/server/solr/factotum/conf/schema.xml && curl 'http://localhost:8983/solr/admin/cores?action=RELOAD&core=factotum&wt=json&indent=true'`

Testing:
`python manage.py shell`

`from haystack.query import SearchQuerySet`
`sqs = SearchQuerySet().all()`
`sqs.count()`