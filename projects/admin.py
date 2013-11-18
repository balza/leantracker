from django.contrib import admin
from projects.models import Project


class ProjectAdmin(admin.ModelAdmin):
 list_display = ('code', 'name', 'expire','enabled')
 search_fields = ['name'] 
 date_hierarchy = 'expire'

admin.site.register(Project,ProjectAdmin)
