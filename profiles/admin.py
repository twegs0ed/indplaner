from django.contrib import admin
from .models import Profile, StanProfile, Operation, Machine
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

class StanProfileAdmin(admin.ModelAdmin):
    list_display = ('user','operation', get_machines, 'pk')
    list_editable = ['operation']
    autocomplete_fields = ['user','operation', 'machines']
    search_fields = ['user','operation',]
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