import django
import os
# settings need setup before calling any Django code
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "factotum.settings")
django.setup()

from dashboard.models import Product

# Get all the products that have stub UPCs.
stub_products = Product.objects.filter(upc__contains="stub")

# Create a variable that will have all products that have non-stub UPCs.
norm_products = Product.objects.exclude(upc__contains="stub")

# Loop through stubs
for stub_product in stub_products:
  ## Find title and compare it to every non-stub product.
  print(stub_product.title)
  ## Determine whether or not there was a match.

  ### There was a match

  ### There was no match