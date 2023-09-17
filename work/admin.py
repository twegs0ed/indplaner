from django.contrib import admin
from .models import Work, WorkForm
from rangefilter.filters import DateRangeFilter
from django.forms import ModelChoiceField


class WorkAdmin(admin.ModelAdmin):
   #change_list_template = "change_form.html"
   
   
   form = WorkForm
   list_display = ('tool', 'user', 'count', 'date', 'text', 'ready')
   list_filter = (('date', DateRangeFilter), 'ready','user',)
   search_fields = ['user', 'tool']
   autocomplete_fields = ('user', 'tool' )

   
admin.site.register(Work, WorkAdmin)
