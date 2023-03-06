from rest_framework import serializers
from structures.models import Structure


class StructureSerializer(serializers.ModelSerializer):

    class Meta:
        # Bind serializer to model
        model = Structure
        # Define fields in model
        fields = ['source', 'identifier', 'path']

    def __init__(self, *args, **kwargs):
        # Call parent constructor
        super().__init__(*args, **kwargs)
        # Set all fields to be readonly
        setattr(self.Meta, 'read_only_fields', [*self.fields])
