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

Check the indices by querying for "alcohol," which should show up in all three:
http://127.0.0.1:9200/_all/_search?q=alcohol

```
{"took":4,"timed_out":false,"_shards":{"total":15,"successful":15,"skipped":0,"failed":0},"hits":{"total":48,"max_score":7.3830523,"hits":[{"_index":"product","_type":"doc","_id":"457","_score":7.3830523,"_source":{"title":"Klean Strip Denatured Alcohol","upc":"stub_457"}},{"_index":"product","_type":"doc","_id":"1749","_score":6.805124,"_source":{"title":"Klean Strip Green Denatured Alcohol","upc":"stub_1749"}},{"_index":"datadocs","_type":"doc","_id":"249215","_score":5.011225,"_source":{"filename":"017553.pdf","title":"Flammable Liquefied Gas Mixture: 1-Butyl Alcohol / 2-Butanol / Ethane / Ethanol / Isobutane / Isob","url":"http://www.airgas.com/msds/017553.pdf"}},{"_index":"datadocument","_type":"doc","_id":"249215","_score":5.011225,"_source":{"filename":"017553.pdf","title":"Flammable Liquefied Gas Mixture: 1-Butyl Alcohol / 2-Butanol / Ethane / Ethanol / Isobutane / Isob","url":"http://www.airgas.com/msds/017553.pdf"}},{"_index":"chemdocs","_type":"doc","_id":"319","_score":4.359831,"_source":{"dsstox":{},"raw_cas":"64-17-5","raw_chem_name":"Alcohol"}},{"_index":"chemdocs","_type":"doc","_id":"357","_score":4.316828,"_source":{"dsstox":{},"raw_cas":"64-17-5","raw_chem_name":"Alcohol"}},{"_index":"chemical","_type":"doc","_id":"319","_score":4.0401006,"_source":{"dsstox":{},"raw_cas":"64-17-5","raw_chem_name":"Alcohol"}},{"_index":"chemical","_type":"doc","_id":"320","_score":4.0401006,"_source":{"dsstox":{},"raw_cas":"64-17-5","raw_chem_name":"Alcohol"}},{"_index":"chemical","_type":"doc","_id":"355","_score":4.0401006,"_source":{"dsstox":{},"raw_cas":"64-17-5","raw_chem_name":"Alcohol"}},{"_index":"chemical","_type":"doc","_id":"356","_score":4.0401006,"_source":{"dsstox":{},"raw_cas":"64-17-5","raw_chem_name":"Alcohol"}}]}}
```

TODO: https://medium.com/@ayarshabeer/django-best-practice-settings-file-for-multiple-environments-6d71c6966ee2
