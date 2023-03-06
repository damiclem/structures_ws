from django.contrib import admin
from .models import Structure


class StructureAdmin(admin.ModelAdmin):
    # Define fields to be displayed
    list_display = 'id', 'source', 'identifier', 'path'
    # Define filter fields
    list_filter = 'source',
    # Define search field
    search_fields = 'identifier',
    # Set all fields readonly
    readonly_fields = 'id', 'source', 'identifier', 'path'

    # Disable add action
    def has_add_permission(self, request, obj=None):
        return False

    # Disable delete action
    def has_delete_permission(self, request, obj=None):
        return False

    # Disable edit action
    def has_change_permission(self, request, obj=None):
        return False


# Register your models here.
admin.site.register(Structure, StructureAdmin)
