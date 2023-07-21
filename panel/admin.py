from django.contrib import admin
from .models import Project
from import_export.admin import ImportExportModelAdmin

@admin.register(Project)
class ProjectAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('id', 'employee', 'employer', 'first_date', 'state')
    list_filter = ('employee', 'state')

