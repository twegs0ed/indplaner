from django.contrib import admin
from .models import Work, WorkForm
from rangefilter.filters import DateRangeFilter
from import_export import resources
from import_export.widgets import ForeignKeyWidget
from import_export.admin import ImportExportModelAdmin
from import_export.widgets import ManyToManyWidget
from import_export.fields import Field
from profiles.models import Machine
from django.contrib.auth.models import User


def full_name(obj):
    return "%s %s" % (obj.user.last_name, obj.user.first_name)
full_name.short_description='Исполнитель'
def get_operation(obj):
    return obj.user.stanprofile.operation
get_operation.short_description='Операция'
def get_machines(obj):
    t=''
    for machine in obj.machines.all():
        t=t+machine.name+' | '
    return t
get_machines.short_description='Станки'

class ForeignKeyWidgetWithCreation (ForeignKeyWidget):

    def clean(self, value, row=None, *args, **kwargs):
        try:
            return super(ForeignKeyWidgetWithCreation, self).clean(value, row, *args, **kwargs)
        except:
            return self.model.objects.create(**{self.field: value})
        

class WorkResource(resources.ModelResource):
    machines = ManyToManyWidget(Machine, separator=', ')
    class Meta:
        model = Work
        fields = ('tool__title', 'user__first_name', 'user__last_name', 'user__stanprofile__operation__name','machines','count')
        export_order = fields
        #Eexclude = ('id',)
        #skip_unchanged=True
        
        #import_id_fields = ('tool')
class WorkAdmin(ImportExportModelAdmin, admin.ModelAdmin):
   resource_class = WorkResource
   form = WorkForm
   list_display = ('tool', full_name, 'count', 'date', 'time', get_operation, get_machines, 'text', 'ready')
   list_filter = (('date', DateRangeFilter), 'ready', 'user__stanprofile__operation' ,'user',)
   search_fields = ['user', 'tool']
   autocomplete_fields = ('user', 'tool', 'machines' )

   
admin.site.register(Work, WorkAdmin)
