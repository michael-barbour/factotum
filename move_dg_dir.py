import os
from pathlib import Path
from django.conf import settings
from dashboard.models import DataGroup

dgs = DataGroup.objects.all()
for dg in dgs:
    # Use the csv file field to get the directory, minus the file name at the end
    old_path, file_name = os.path.split(dg.csv.path)
    print("oldpath " + str(old_path))

    # Construct the Path for the new file location
    new_path = Path(settings.MEDIA_ROOT + '/' + str(dg.pk))
    print("newpath " + str(new_path))

    try:
        # Rename the DG directory
        os.rename(old_path, str(new_path))

        # Save the new CSV file name to the model
        new_name = Path(str(dg.pk) + '/' + file_name)
        dg.csv.name = str(new_name)

        # Save the new Zip file name to the model if it exists
        if dg.zip_file:
            zip_path, zip_file_name = os.path.split(dg.zip_file)
            new_zip_name = Path(settings.MEDIA_URL + "/" + str(dg.pk) + "/" + zip_file_name)
            dg.zip_file = str(new_zip_name)

        # Ensure the changes are saved
        dg.save()
        print(str(dg.csv.path))
        print(dg.zip_file)

    except FileNotFoundError:
        print("File path not found for DG: " + str(dg.pk))
