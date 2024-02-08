from django.contrib import admin
from .models import Material

# Register your models here.

class MaterialAdmin(admin.ModelAdmin):
    list_display = ['title']
    search_fields = ['title',]
    
admin.site.register(Material, MaterialAdmin)