from structures.models import Structure
from django.db import transaction
from glob import iglob
import server.settings as env
import os
import re

af_version = env.AF_VERSION
# Map source database -> regex for local path
source_paths = {
    'PDB': '/mnt/db/mmCIF/*/{0:}.cif.gz',
    'UniProtKB': '/mnt/db/af/*_v' + af_version + '/AF-{0:}-F1-model_v' + af_version + '.cif.gz'
}


@transaction.atomic
def run(*args):
    # Initialize counter
    counter_pdb, counter_upt = 0, 0
    # TODO Clear database
    Structure.objects.all().delete()
    # Loop through each source database
    for source_id, source_path in source_paths.items():
        # Define files iterator
        path_iterator = iglob(source_path.format('*'))
        # Loop through each file
        for file_path in path_iterator:
            # Get file name
            file_name = os.path.basename(file_path)
            # Define RegEx for file name
            # _, file_regex = os.path.split(source_path)
            file_regex = source_path
            file_regex = file_regex.replace('*', '.+')
            file_regex = file_regex.format('([0-9a-zA-Z]+)')
            # Extract id out of file name
            structure_id = re.match(file_regex, file_path).group(1)
            # TODO Store structure
            structure = Structure(source=source_id, identifier=structure_id, path=file_path)
            structure.save()
            # TODO Remove this
            print("--------------------")
            print("File path:", file_path)
            print("File name:", file_name)
            print("Source id:", source_id)
            print("Item id:", structure_id)
            print("--------------------")
            # TODO Remove this
            counter_pdb += 1 if source_id == 'PDB' else 0
            counter_upt += 1 if source_id == 'UniProtKB' else 0

    print(f"Read {counter_pdb} entries from PDB")
    print(f"Read {counter_upt} entries from UniProtKB")
