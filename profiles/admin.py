from django.contrib import admin
from .models import Profile, StanProfile, Operation, Machine
from import_export.admin import ExportActionMixin, ImportExportModelAdmin
from import_export import resources
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('bio','pk')
    ordering = ['bio']
    search_fields = ['bio']


def get_machines(obj):
    t=''
    for machine in obj.machines.all():
        t=t+machine.name+' | '
    return t
get_machines.short_description='Станки'
def get_username(obj):
    
    return obj.user.first_name+' '+obj.user.last_name
get_username.short_description='ФИО'




class StanProfileResource(resources.ModelResource):
    
    class Meta:
        model = StanProfile

        fields = ('user__first_name', 'user__last_name', 'machines')
        #export_order = ('tool', 'count')
        exclude = ('id',)
        #import_id_fields = ('tool', 'count')
    def dehydrate_machines(self, obj):
        t=''
        for machine in obj.machines.all():
            t=t+machine.name+' ; '
        return t 





class StanProfileAdmin(ExportActionMixin, admin.ModelAdmin):
    resource_class = StanProfileResource
    list_display = ('user', get_username, 'operation',  get_machines, 'pk')
    list_editable = ['operation']
    autocomplete_fields = ['user','operation', 'machines']
    search_fields = ['user__first_name','user__last_name', 'user__username','operation__name',]
    pass
class OperationAdmin(admin.ModelAdmin):
    search_fields = ['name',]
    pass
class MachineAdmin(admin.ModelAdmin):
    search_fields = ['name',]
    pass
admin.site.register(Profile, ProfileAdmin)
admin.site.register(StanProfile, StanProfileAdmin)
admin.site.register(Operation, OperationAdmin)
admin.site.register(Machine, MachineAdmin)