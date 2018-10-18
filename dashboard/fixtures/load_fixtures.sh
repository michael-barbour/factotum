python manage.py flush

python manage.py makemigrations
python manage.py migrate
# specialP@55word
python manage.py loaddata 00_superuser 01_lookups \
    02_datasource 03_datagroup 04_PUC 05_product \
    06_datadocument 07_script 08_extractedtext \
    09_productdocument 10_extractedchemical \
    11_dsstoxsubstance 12_habits_and_practices\
    13_habits_and_practices_to_puc 14_product_to_puc\
    15_extractedfunctionaluse 16_producttag


# some shells prefer one line
python manage.py loaddata 00_superuser 01_lookups 02_datasource 03_datagroup 04_PUC 05_product 06_datadocument 07_script 08_extractedtext   09_productdocument 10_extractedchemical  11_dsstoxsubstance 12_habits_and_practices 13_habits_and_practices_to_puc 15_extractedfunctionaluse.yaml 16_extractedcpcat.yaml 17_extractedlistpresence.yaml
python manage.py loaddata 00_superuser 01_lookups 02_datasource 03_datagroup 04_PUC 05_product 06_datadocument 07_script 08_extractedtext   09_productdocument 10_extractedchemical  11_dsstoxsubstance 12_habits_and_practices 13_habits_and_practices_to_puc 14_product_to_puc 15_extractedfunctionaluse 16_producttag