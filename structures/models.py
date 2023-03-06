from django.db import models


class Structure(models.Model):
    # Source database
    source = models.CharField(max_length=10)
    # Unique identifier of a protein
    # NOTE there might be multiple files for a single identifier (versioning)
    identifier = models.CharField(max_length=20)
    # Absolute path to file
    path = models.CharField(max_length=100, unique=True)

    class Meta:
        # Setup indexing
        indexes = [
            models.Index(fields=['identifier'], name='identifier_index'),
            # models.Index(fields=['-source'], name='source_index'),
            # models.Index(fields=['-path'], name='path_index')
        ]
        # Setup ordering
        ordering = ['identifier', '-path']
