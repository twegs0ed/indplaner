from django.contrib import admin
from .models import Workplace
class WorkplaceAdmin(admin.ModelAdmin):
    list_display = ('name','text')
    search_fields = ['name', 'text']
    ordering = ['name']
admin.site.register(Workplace, WorkplaceAdmin)