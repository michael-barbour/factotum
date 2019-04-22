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