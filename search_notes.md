## In your development environment

Launch elastiscsearch 6.6:
`/usr/local/opt/elasticsearch@6.6/bin/elasticsearch`

Check:
http://127.0.0.1:9200/

Then launch kibana:
`kibana`
Check:
http://127.0.0.1:5601/

http://127.0.0.1:9200/_cat/indices?v

`python manage.py search_index --rebuild`

Queries to test:

```
GET /_cat/indices/*

GET /factotum_chemicals/_mapping

GET /factotum_chemicals/_search/
{
    "query": {
      "query_string" : {
            "query" : "alcohol" 
        }
    }
}

GET /factotum_chemicals/_search/
{
    "query": {
        "query_string" : {
            "default_field" : "raw_chem_name",
            "query" : "alcohol"
        }
    }
}

GET /factotum_chemicals/_search/
{
    "query": {
        "query_string" : {
            "default_field" : "raw_cas",
            "query" : "64-17-5"
        }
    }
}

GET /factotum_chemicals/_search/
{
    "query": {
        "query_string" : {
            "default_field" : "dsstox.true_chemname",
            "query" : "ethanol"
        }
    }
}

```

## Loading documents as JSON

To add these same documents to a different index (for example, if you want to test the serialized seed data without running the serialization script), build a JSON object formatted for the `_bulk` endpoint. 

```
# All the results, but without any of the _meta fields
GET /factotum_chemicals/_search/?filter_path=hits.hits._source
```
This will get part of the way there, but the formatting of the JSON in the bulk command needs to be collapsed into single lines, and each document will need its own command line.

run this `POST` URL:
```


# Bulk-loading JSON objects into an index
POST /factotum_chemicals_fake/_bulk
{ "index" : {"_index": "factotum_chemicals_fake","_type": "_doc"}}
{"facet_model_name" : "Chemical","data_document_id" : 178577,"product_count" : 0,"raw_cas" : "520-45-6","dsstox" : { },"raw_chem_name" : "Dehydroacetic acid"}
{ "index" : {"_index": "factotum_chemicals_fake","_type": "_doc"}}
{"facet_model_name" : "Chemical","data_document_id" : 156051,"product_count" : 0,"raw_cas" : "80-05-7","dsstox" : {"true_cas" : "80-05-7","true_chemname" : "bisphenol a"},"raw_chem_name" : "bisphenol a"}

GET /factotum_chemicals_fake/_search/
```

Cleanup:

```
DELETE /factotum_chemicals_fake
```