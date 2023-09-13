from django.contrib import admin
from .models import Work, WorkForm
from rangefilter.filters import DateRangeFilter

# Register your models here.c\
class WorkAdmin(admin.ModelAdmin):
   #change_list_template = "change_form.html"
   form = WorkForm
   #list_display = ('user', 'tool', 'count', 'date', 'text')
   list_filter = (('date', DateRangeFilter), 'user',)
   search_fields = ['user', 'tool']
   
admin.site.register(Work, WorkAdmin)
