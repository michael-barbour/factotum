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

        # Build list of UPC product names
        list_upc_names = []
        list_upc_pks = []
        for norm_product in norm_products:
            norm_prod = norm_product.title.lower()
            list_upc_names.append(norm_prod)
            pk_product = norm_product.pk
            list_upc_pks.append(pk_product)

        # Open file that will contain the top match for each stub product
        file_top_yaml = open("top_match.yaml", 'w')

        # Open file that will contain matching scores for the process.extract method
        file_multi_yaml = open("multi_matches.yaml", "w")

        # Set the number of matches ordered by scores.  By default this number is 5.
        num_matches = 3

        # Set the threshold value to use for the matching score.  This value will be used for each stub product
        # that is compared to every UPC product. Adjust this parameter to a desired threshold. This parameter has
        # a default value of 0 if not set by the user.  Matching scores below this value will not appear in the results.
        cutoff = 80

        # YAML related variables.
        str_stub = 'Stub Product'
        str_upc = 'UPC Product'
        list_yaml = []
        list_multi_yaml = []

        # Loop through stubs
        for stub_product in stub_products:
            ## Find title and compare it to every non-stub product.
            stub_prod = stub_product.title.lower()
            stub_prod_pk = stub_product.pk
            stub_prod = stub_prod + "; pk = " + str(stub_prod_pk)   # Attach pk to stub product name.

            # Get a list of matches ordered by scores, using the fuzz.token_set_ratio matching , to get all num_matches.
            # Note:  there are 4 popular types of fuzzy matching logic supported by the fuzzywuzzy package.  They are:
            # ratio, partial ratio, token sort ratio, and token set ratio.  Opted to use the token set ratio because it
            # gives me the best scores and matches.  That said, the user can set the scorer to any other matching method
            # if wished.
            list_multi = process.extract(stub_prod, list_upc_names, scorer=fuzz.token_set_ratio, limit=num_matches)
            
            # Convert list to a dictionary.
            multi_dict = dict(list_multi)
            
            # Declare empty list
            temp_list = []
            
            # Loop over items in dictionary and attach the pks to the names of the UPC products.
            for key, value in multi_dict.items():
                i_upc = list_upc_names.index(key)                     # Locate upc name in original list.
                new_key = key + "; pk = " + str(list_upc_pks[i_upc])  # Attach pk to keyname.
                multi_dict[new_key] = multi_dict.pop(key)             # Replace old key with new one.
                temp_list.append({new_key: value})                    # Create list with modified keynames.

            upc_dict = {str_upc: temp_list}                           # Define upc dictionary.
            stub_dict = {stub_prod: [upc_dict]}                       # Define stub dictionary.
            list_multi_yaml.append(stub_dict)                         # Append dictionary to list.

            # Get the top one match, using the fuzz.token_set_ratio matching and a threshold value.
            list_one = process.extractOne(stub_prod, list_upc_names, scorer=fuzz.token_set_ratio, score_cutoff=cutoff)

            # Check whether a match was found.  If a match is not found, print appropriate message to output.
            # If match is found, attach pk number to UPC product name and format results using dictionaries and
            # lists.
            if list_one is None:
                upc_dict = {str_upc: ['No matches found.']}
                stub_upc_dict = {stub_prod: [upc_dict]}
            else:
                i_upc = list_upc_names.index(list_one[0])
                upc_pk_str = list_one[0] + "; pk = " + str(list_upc_pks[i_upc])
                upc_pk_dict = {upc_pk_str: list_one[1]}
                list1 = [upc_pk_dict]
                upc_dict = {str_upc: list1}
                stub_upc_dict = {stub_prod: [upc_dict]}

            # Append dictionaries to list.
            list_yaml.append(stub_upc_dict)

        # Write top match results to output.
        top_match_doc = {str_stub: list_yaml}
        yaml.safe_dump(top_match_doc, file_top_yaml, default_flow_style=False)

        # Write multiple matches results to output file.
        multi_match_doc = {str_stub: list_multi_yaml}
        yaml.safe_dump(multi_match_doc, file_multi_yaml, default_flow_style=False)

        # Close files
        file_top_yaml.close()
        file_multi_yaml.close()
