import django
import os
# settings need setup before calling any Django code
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "factotum.settings")
django.setup()

from dashboard.models import Product
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

# Get all the products that have stub UPCs.
stub_products = Product.objects.filter(upc__contains="stub")

# Create a variable that will have all products that have non-stub UPCs.
norm_products = Product.objects.exclude(upc__contains="stub")

# Open file that will contain matches with high scores
filehs = open("matches_high_scores.txt", 'w')

# Open file that will contain matches with low scores
filels = open("matches_low_scores.txt", 'w')

# Loop through stubs
for stub_product in stub_products:
    ## Find title and compare it to every non-stub product.
    # print(stub_product.title)
    stub_prod = stub_product.title.lower()
    score = 0.0
    norm_prod1 = ''
    msg = ''
    ## Determine whether or not there was a match.
    for norm_product in norm_products:
        norm_prod = norm_product.title.lower()
        score1 = fuzz.token_sort_ratio(stub_prod, norm_prod)  # Calculate score
        if score1 > score:
            score = score1
            norm_prod1 = norm_prod
     ### There was a match (high score)
    if score > 80.0:
        msg = 'stub_product = ' + stub_prod + ', upc_product = ' + norm_prod1 + ', score = ' + str(score) + '\n'
        filehs.write(msg)
    else:   ### Low score matches
        msg = 'stub_product = ' + stub_prod + ', upc_product = ' + norm_prod1 + ', score = ' + str(score) + '\n'
        filels.write(msg)

# Close files
filehs.close()
filels.close()
