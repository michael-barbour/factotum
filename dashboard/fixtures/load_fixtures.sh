python manage.py flush

python manage.py makemigrations
python manage.py migrate
# specialP@55word
python manage.py loaddata 00_superuser \
    01_lookups 02_datasource 03_datagroup \
    04_PUC 05_product 06_datadocument  \
    07_script 08_extractedtext 16_extractedcpcat \
    09_productdocument 065_rawchem_etc \
    11_dsstoxsubstance 12_habits_and_practices \
    13_habits_and_practices_to_puc 14_product_to_puc 18_puc_tag


# some shells prefer one line
python manage.py loaddata 00_superuser 01_lookups 02_datasource 03_datagroup 04_PUC 05_product 06_datadocument  07_script 08_extractedtext 16_extractedcpcat 09_productdocument 065_rawchem_etc 11_dsstoxsubstance 12_habits_and_practices 13_habits_and_practices_to_puc 14_product_to_puc   18_puc_tag
