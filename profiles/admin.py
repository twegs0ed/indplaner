from django.contrib import admin
from .models import Profile
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('bio','pk')
    ordering = ['bio']
    search_fields = ['bio']
admin.site.register(Profile, ProfileAdmin)