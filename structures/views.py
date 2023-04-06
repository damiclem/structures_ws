from structures.models import Structure
from django.http import FileResponse
from rest_framework import exceptions, views
from .utils import iter_cif
import server.settings as env
import requests
import gzip
import os
import re
import io


class StructureFileView(views.APIView):

    def get(self, request, source: str, identifier: str, model: int = None, chain: str = None):
        """
        Retrieve MMCIF file associated to source and identifier. Extract only given model and/or chain, when provided.
        """
        # Try retrieving file from local path
        file_path_or_url = self.get_local_file_path(source, identifier)
        # Otherwise, try retrieving file from remote url
        if file_path_or_url is None:
            # Get path from URL
            file_path_or_url = self.get_remote_file_url(source, identifier, version=env.AF_VERSION)
        # Initialize output file handler
        out_handle = io.BytesIO()
        # Try retrieving structure/model/chain
        try:
            # Retrieve input file handle (must be string!)
            in_handle = self.get_file_handle(file_path_or_url)
            # Write header
            out_handle.write(f'data_{identifier}\n#\n_entry.id   {identifier}\n'.encode('utf-8'))
            # Atom line intercepted
            atom_found = False
            # Write lines
            for is_atom, curr_line in iter_cif(in_handle, model, chain):
                # Cast line to bytes
                out_handle.write(curr_line.encode('utf-8'))
                # Check if atom has been found
                atom_found = atom_found or is_atom
            # Close input handle
            in_handle.close()
            # Handle atom not found
            if not atom_found:
                # Case model has been requested
                if model is not None:
                    raise exceptions.NotFound(f'Model {model} not found in structure {identifier} from {source}')
                # Case chain has been requested
                if chain is not None:
                    raise exceptions.NotFound(f'Chain {chain} not found in structure {identifier} from {source}')
        # Handle HTTP errors
        except exceptions.APIException as e:
            # Just raise it
            raise e
        # Handle other exceptions
        except Exception as e:
            # Raise structure not found
            raise exceptions.NotFound(detail=f"Structure {identifier} not found in {source}")
        # Get output file size
        out_handle.seek(0, io.SEEK_END)
        out_size = out_handle.tell()
        # Reset output file handler
        out_handle.seek(0)
        # Return response
        response = FileResponse(out_handle, content_type='text/plain')
        response['Content-Length'] = out_size
        response['Content-Disposition'] = "inline"  # ; filename={}".format(os.path.basename(file))
        # Send response back
        return response

    # Try retrieving file from local database
    def get_local_file_path(self, source: str, identifier: str) -> str:
        # Initialize local file path
        file_path = None
        # Try retrieving structure from database
        try:
            structure = Structure.objects.get(identifier=identifier, source=source)
            # Check file path exists
            if os.path.isfile(structure.path):
                # Set file path
                file_path = structure.path
        except Structure.DoesNotExist:
            # Unset file path
            file_path = None
        # Return retrieved path
        return file_path

    # Try retrieving file from remote database
    def get_remote_file_url(self, source: str, identifier: str, version: int = None) -> str:
        # Initialize remote file URL
        file_url = None
        # Define file URL for structure in PDB RCSB
        if source == "PDB":
            file_url = f"https://files.rcsb.org/download/{identifier.lower()}.cif.gz"
        # Define file URL for structure in AlphaFoldDB
        if source == "UniProtKB":
            file_url = f"https://alphafold.ebi.ac.uk/files/AF-{identifier.lower()}-F1-model_v{version}.cif"
        # Return URL for remote file
        return file_url

    # Try retrieving file from either remote URL or local path
    def get_file_handle(self, path_or_url: str):
        # Initialize file handle
        file_handle = None
        # Handle remote file URL
        if re.match(r'https?://', path_or_url):
            # Initialize file handle
            file_handle = io.BytesIO()
            # Retrieve remote file
            with requests.get(path_or_url, stream=True) as response:
                # Raise error, if any
                response.raise_for_status()
                # Loop through each chunk in response
                for chunk in response.iter_content(chunk_size=1024):
                    # Write output file stream
                    file_handle.write(chunk)
                # Reset file handler
                file_handle.seek(0)
        # Handle local file path
        else:
            file_handle = open(path_or_url, 'rb')
        # Handle zipped files
        if re.match(r'.*.gz$', path_or_url):
            # Unzip file
            file_handle = gzip.open(file_handle, 'rt')
        # Return file handle
        return file_handle
