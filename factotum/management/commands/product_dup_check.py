import django
import os
import yaml

from django.core.management.base import BaseCommand

# settings need setup before calling any Django code
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "factotum.settings")
django.setup()

from dashboard.models import Product

# Import the fuzzywuzzy package/libraries.
from fuzzywuzzy import fuzz
from fuzzywuzzy import process


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        help = 'Score stub product titles'

        # Get all the products that have stub UPCs.
        stub_products = Product.objects.filter(upc__contains="stub")

        # Create a variable that will have all products that have non-stub UPCs.
        norm_products = Product.objects.exclude(upc__contains="stub")

        # Open file that will contain the top match for each stub product
        file_topmatch = open("top_match.txt", "w")

        # Open file that will contain matching scores for the process.extractOne method
        file_multimatches = open("multi_matches.txt", "w")

        file_yaml = open("document.yaml", 'w')

        # Set the number of matches ordered by scores.  By default this number is 5.
        num_matches = 3

        # Set the threshold value to use for the matching score.  This value will be used for each stub product
        # that is compared to every UPC product. Adjust this parameter to a desired threshold. This parameter has
        # a default value of 0 if not set by the user.  Matching scores below this value will not appear in the results.
        cutoff = 10

        str_stub = 'Stub Product'
        list_yaml = []

        # Loop through stubs
        for stub_product in stub_products:
            ## Find title and compare it to every non-stub product.
            stub_prod = stub_product.title.lower()

            # Write stub product title to files.
            file_multimatches.write(stub_prod + "\n")
            file_topmatch.write(stub_prod + "\n")

            # Get a list of matches ordered by scores, using the fuzz.token_set_ratio matching , to get all num_matches.
            # Note:  there are 4 popular types of fuzzy matching logic supported by the fuzzywuzzy package.  They are:
            # ratio, partial ratio, token sort ratio, and token set ratio.  Opted to use the token set ratio because it
            # gives me the best scores and matches.  That said, the user can set the scorer to any other matching method
            # if wished.
            list_multi = process.extract(stub_prod, norm_products, scorer=fuzz.token_set_ratio, limit=num_matches)

            # Get the top one match, using the fuzz.token_set_ratio matching and a threshold value.
            list_one = process.extractOne(stub_prod, norm_products, scorer=fuzz.token_set_ratio, score_cutoff=cutoff)
            my_tuple = (('UPC_Product -> ' + str(list_one[0]), list_one[1]),)
            my_dict = dict(my_tuple)
            my_dict1 = {stub_prod: my_dict}
            list_yaml.append(my_dict1)

            # Write matches and their scores to files.  Note that the lists have to be converted to strings before
            # writing the data to a file.
            file_multimatches.write(' '.join(str(x) for x in list_multi) + "\n\n")
            file_topmatch.write(str(list_one) + "\n\n")

        my_document = {str_stub: list_yaml}
        yaml.safe_dump(my_document, file_yaml, default_flow_style=False)


        # Close files
        file_topmatch.close()
        file_multimatches.close()
        file_yaml.close()
