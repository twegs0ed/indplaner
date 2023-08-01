from django.contrib import admin
from .models import Workplace
class WorkplaceAdmin(admin.ModelAdmin):
    list_display = ('name','machine')
    search_fields = ['name', 'machine']
    ordering = ['name']
admin.site.register(Workplace, WorkplaceAdmin)