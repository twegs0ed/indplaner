from django.contrib import admin
from .models import Work, WorkForm
from rangefilter.filters import DateRangeFilter
from import_export import resources
from import_export.widgets import ForeignKeyWidget
from import_export.admin import ImportExportModelAdmin
from import_export.widgets import ManyToManyWidget, CharWidget
from import_export.fields import Field
from profiles.models import Machine
from django.contrib.auth.models import User
from order.models import Order
from django.utils.html import format_html
from datetime import datetime
from tools.models import Toolsonwarehouse


def full_name(obj):
    return "%s %s" % (obj.user.last_name, obj.user.first_name)
full_name.short_description='Исполнитель'
def get_operation(obj):
    return obj.user.stanprofile.operation
get_operation.short_description='Операция'
'''def get_machines(obj):
    t=''
    for machine in obj.machines.all():
        t=t+machine.name+' | '
    return t
get_machines.short_description='Станки'
'''

class ForeignKeyWidgetWithCreation (ForeignKeyWidget):

    def clean(self, value, row=None, *args, **kwargs):
        try:
            return super(ForeignKeyWidgetWithCreation, self).clean(value, row, *args, **kwargs)
        except:
            return self.model.objects.create(**{self.field: value})
        

class WorkResource(resources.ModelResource):
    machines = ManyToManyWidget(Machine, separator=', ')
    firm = Field()
    machines = Field()
    

    def before_export(self, queryset, *args, **kwargs):
        self.firm='1'
        return self
    class Meta:
        model = Work
        fields = ('tool__title', 'user__first_name', 'user__last_name', 'date', 'user__stanprofile__operation__name','count', 'firm','machines')
        export_order = fields
        #Eexclude = ('id',)
        #skip_unchanged=True
    def dehydrate_firm(self, work):
        o=Order.objects.filter(tool=work.tool).order_by('-exp_date', '-order_date_worker').all()[:1]
        t=""
        for l in o: 
            
            if l.firm:
                t+=l.firm.title
                t+='\n'
                if l.exp_date:t+=' срок '+datetime.strftime(l.exp_date, '%d.%m.%Y')
                #t+=' - '+str(l.count)+' шт. ()'
        return t
    def dehydrate_machines(self, work):
        ms=work.machines.all()
        if ms:
            t=""
            for m in ms:
                t+=m.name+' ()'
        else: t='отсутствует'
        
        return t
        
        #import_id_fields = ('tool')
class WorkAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = WorkResource
    form = WorkForm
    list_display = ('tool', full_name, 'count', 'date', 'time', get_operation, 'get_machines', 'text', 'ready', 'ord')
    list_filter = (('date', DateRangeFilter), 'ready', 'user__stanprofile__operation', 'machines' ,'user')
    search_fields = ['user__username', 'user__first_name','user__last_name', 'tool__title']
    autocomplete_fields = ('user', 'tool' )
    def get_machines(self, obj):
        return ",".join([str(p) for p in obj.machines.all()])
    get_machines.short_description = "Станки"
    def ord(self, obj):
        o=Order.objects.filter(tool=obj.tool).order_by('-exp_date', '-order_date_worker').all()[:1]

        t=""
        for l in o: 
            
            if l.firm:
                t+='<p style="background-color:;"><font color="">'+l.firm.title+'</font> '
                if l.exp_date:t+=datetime.strftime(l.exp_date, '%d.%m.%Y')
                t+=' - '+str(l.count)+' шт. '
                t+='<br></p>'

        return format_html(t)
    ord.short_description = "Изделие"

   
admin.site.register(Work, WorkAdmin)
