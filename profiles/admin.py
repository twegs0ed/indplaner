from django.contrib import admin
from .models import Profile, StanProfile, Operation
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('bio','pk')
    ordering = ['bio']
    search_fields = ['bio']
class StanProfileAdmin(admin.ModelAdmin):
    pass
class OperationAdmin(admin.ModelAdmin):
    pass
admin.site.register(Profile, ProfileAdmin)
admin.site.register(StanProfile, StanProfileAdmin)
admin.site.register(Operation, OperationAdmin)