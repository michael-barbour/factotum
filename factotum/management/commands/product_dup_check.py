import django
import os
import yaml
import warnings

# Ignore this specific warning.  It is not crucial to use the Levenshtein library for this script.
warnings.filterwarnings("ignore", message="Using slow pure-python SequenceMatcher. Install python-Levenshtein to remove this warning")

from django.core.management.base import BaseCommand

# settings need setup before calling any Django code
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "factotum.settings")
django.setup()

from dashboard.models import Product

# Import the fuzzywuzzy package/libraries.
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

# Import the ruamel.yaml package.  This is a YAML loader/dumper package for Python.
from ruamel.yaml import YAML

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

        # Get current working directory
        pathname = os.getcwd()

        # Open file that will contain the top match for each stub product
        file_top_yaml = open(pathname + "\\top_match.yaml", 'w')

        # Open file that will contain matching scores for the process.extract method
        file_multi_yaml = open(pathname + "\\multi_matches.yaml", "w")

        # Set the number of matches ordered by scores.  By default this number is 5.
        num_matches = 3

        # Set the threshold value to use for the matching score.  This value will be used for each stub product
        # that is compared to every UPC product. Adjust this parameter to a desired threshold. This parameter has
        # a default value of 0 if not set by the user.  Matching scores below this value will not appear in the results.
        cutoff = 80

        # YAML related variables.
        yaml_top = YAML()
        yaml_multi = YAML()
        list_yaml = []
        list_multi_yaml = []

        # Loop through stubs
        for stub_product in stub_products:
            ## Find title and compare it to every non-stub product.
            stub_prod1 = stub_product.title.lower()
            stub_prod = stub_prod1.replace(":", "").replace("\t", "")
            stub_prod_pk = stub_product.pk

            # Initialize stub product string that will be used for the YAML strings below.
            stub_str = "stub product: " + stub_prod + "\npk_stub: " + str(stub_prod_pk)

            # Get a list of matches ordered by scores, using the fuzz.token_set_ratio matching , to get all num_matches.
            # Note:  there are 4 popular types of fuzzy matching logic supported by the fuzzywuzzy package.  They are:
            # ratio, partial ratio, token sort ratio, and token set ratio.  Opted to use the token set ratio because it
            # gives me the best scores and matches.  That said, the user can set the scorer to any other matching method
            # if wished.
            list_multi = process.extract(stub_prod, list_upc_names, scorer=fuzz.token_set_ratio, limit=num_matches)

            # Convert list to a dictionary.
            multi_dict = dict(list_multi)

            # Set counter of upc products to zero.
            upc_counter = 0
            # Initialize YAML string to stub product string.
            yaml_str = stub_str
            # Loop over items in dictionary and build YAML string for output.  Note that we are not duplicating keys:
            # we are attaching an index to the upc products's names and pks.  Duplication of keys can be allowed by
            # setting yaml.allow_duplicate_keys to TRUE.
            for key, value in multi_dict.items():
                i_upc = list_upc_names.index(key)                     # Locate upc name in original list.
                upc_counter += 1                                      # Use counter as index for the matched UPCs.
                new_key = key.replace(":", "").replace("\t", "")      # Remove colons and tabs from titles.
                yaml_str = yaml_str + "\nupc product" + str(upc_counter) + ": " + new_key + \
                           "\npk_upc" + str(upc_counter) + ": " + str(list_upc_pks[i_upc]) + \
                           "\nscore" + str(upc_counter) + ": " + str(value)

            data1 = yaml_multi.load(yaml_str)                     # Load data into YAML object.
            list_multi_yaml.append(data1)                         # Append dictionary/data to list.

            # Get the top one match, using the fuzz.token_set_ratio matching and a threshold value.
            list_one = process.extractOne(stub_prod, list_upc_names, scorer=fuzz.token_set_ratio, score_cutoff=cutoff)

            # Check whether a match was found.  If a match is not found, print appropriate message to output.
            # If match is found, build YAML string using stub and upc products' names and pks.
            if list_one is None:
                yaml_str = stub_str + "\nupc product: " + "no matches found"
            else:
                i_upc = list_upc_names.index(list_one[0])
                yaml_str = stub_str + "\nupc product: " + list_one[0] + "\npk_upc: " + str(list_upc_pks[i_upc]) + \
                           "\nscore: " + str(list_one[1])

            # Load data into YAML object.
            data2 = yaml_top.load(yaml_str)

            # Append data/dictionary to list.
            list_yaml.append(data2)

        # Write top match results to output file.
        yaml_top.dump(list_yaml, file_top_yaml)
        print("Top match results were output to " + file_top_yaml.name)

        # Write multiple matches results to output file.
        yaml_multi.dump(list_multi_yaml, file_multi_yaml)
        print("Multiple results were output to " + file_multi_yaml.name)

        # Close files
        file_top_yaml.close()
        file_multi_yaml.close()
