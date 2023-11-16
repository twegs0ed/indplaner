from django.contrib import admin
from rangefilter.filters import DateRangeFilter, DateTimeRangeFilter
from .models import Toolsonwarehouse, Tools, Rec_Tools, Priem, Workplace
from profiles.models import Profile
from order.models import Order
from import_export.admin import ExportActionMixin, ImportExportModelAdmin
from import_export import resources
from import_export.fields import Field
from django.utils.html import format_html
from import_export.widgets import ForeignKeyWidget, CharWidget
from django.db import models
from django.forms import TextInput, Textarea
import re


def order_it(modeladmin, request, queryset):
    for obj in queryset:
        i=Order.get_count_ordered(obj)
        ord=Order()
        '''c_ord=get_object(Order,obj)
        if c_ord:
            c_ord.delete()'''
        ord.tool=obj
        ord.worker=Profile.objects.get(pk=10)
        ord.count=obj.min_count-obj.count-i
        ord.save()

def get_object(self, obj):
    try:
        return Order.objects.filter(tool=obj)
    except Order.DoesNotExist:
        return False


order_it.short_description = "В заявку"

class ToolsResource(resources.ModelResource):
    
   

    class Meta:
        model = Tools
        
        fields = ('tool__title', 'count','worker__bio', 'giveout_date')
        export_order = ('tool__title', 'worker__bio', 'count')

class ForeignKeyWidgetWithCreation (ForeignKeyWidget):

    def clean(self, value, row=None, *args, **kwargs):
        try:
            return super(ForeignKeyWidgetWithCreation, self).clean(value, row, *args, **kwargs)
        except:
            return self.model.objects.create(**{self.field: value})
        
class ToolsonwarehouseResource(resources.ModelResource):
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows':5, 'cols':40})},
    }
    #tool = Field(attribute='title', column_name='title', widget=CharWidget(),)
    
    workplace = Field(
        column_name='workplace',
        attribute='workplace',
        widget=ForeignKeyWidgetWithCreation(model=Workplace, field='name'))
    
    class Meta:
        model = Toolsonwarehouse
        #skip_unchanged=False
        fields = ('title', 'count', 'workplace__name','material', 'stock_sizes', 'count_in_one_stock', 'cover' )
        exclude = ('id',)
        export_order = ('title','count', 'workplace')
        import_id_fields=['title']
        #import_id_field = 'title'
    
        
class ToolsonwarehouseAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows':5, 'cols':40})},
    }
    resource_class = ToolsonwarehouseResource
    #autocomplete_fields = ['tool']
    #readonly_fields = ('need_count',)
    list_display = ('title', 'count', 'workplace', 'created_date', 'text', 'cover')
    list_filter = ('workplace',)
    search_fields = ['title']
    ordering = ['title', 'created_date']
    #actions = [order_it]
    list_editable = ['text']
    def get_search_results(self, request, queryset, search_term):
        search_term=str(search_term).upper()
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        return queryset, use_distinct


class ToolsAdmin(ExportActionMixin, admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows':5, 'cols':40})},
    }
    #raw_id_fields = ('worker', 'tool')
    autocomplete_fields = ['tool','worker']
    resource_class = ToolsResource
    list_display = ('tool', 'worker', 'count', 'giveout_date', 'text')
    list_filter = (('giveout_date', DateRangeFilter), 'worker')
    search_fields = ['tool__title', 'worker__bio']
    ordering = ['-giveout_date']
    list_editable = ['text']
    def get_search_results(self, request, queryset, search_term):
        #print(search_term)
        #search_term=re.sub("[^\d\.]", "", str(search_term))
        search_term=str(search_term).upper()
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        #queryset |= self.model.objects.filter(tool__title=search_term)
        return queryset, use_distinct
    

    pass
class Rec_ToolsAdmin(ExportActionMixin, admin.ModelAdmin):
    #raw_id_fields = ('worker', 'tool')
    autocomplete_fields = ['worker', 'tool']
    resource_class = ToolsResource
    list_display = ('worker', 'tool', 'count', 'giveout_date')
    list_filter = (('giveout_date', DateRangeFilter), 'worker', 'tool')
    search_fields = ['tool__title', 'worker__bio']
    ordering = ['-giveout_date']
    pass
class ToolsdeficiteAdmin(admin.ModelAdmin):
    pass
class PriemResource(resources.ModelResource):
    tool = Field(
        column_name='tool',
        attribute='tool',
        widget=ForeignKeyWidgetWithCreation(model=Toolsonwarehouse, field='title'))
    #firm = Field(
        #column_name='firm',
        #attribute='firm',
        #widget=ForeignKeyWidgetWithCreation(model=Firm, field='title'))
    class Meta:
        model = Priem

        fields = ('tool', 'count','place','giveout_date','text')
        export_order = ('tool', 'count')
        exclude = ('id',)
        import_id_fields = ('tool', 'count')

class PriemAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = PriemResource
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows':5, 'cols':40})},
    }
    autocomplete_fields = ['tool', 'place','worker']
    list_display = ('tool', 'count', 'giveout_date', 'text')
    #list_filter = (('giveout_date', DateRangeFilter))
    list_filter = (('giveout_date', DateRangeFilter),)
    search_fields = ['tool__title']
    list_editable = ['text']
    def get_search_results(self, request, queryset, search_term):
        search_term=str(search_term).upper()
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        
        
        try:
            search_term_as_int = int(search_term)
        except ValueError:
            pass
        else:
            queryset |= self.model.objects.filter(tool=search_term_as_int)
        return queryset, use_distinct
    pass

admin.site.register(Tools, ToolsAdmin)
admin.site.register(Priem, PriemAdmin)
admin.site.register(Toolsonwarehouse, ToolsonwarehouseAdmin)
#admin.site.register(Rec_Tools, Rec_ToolsAdmin)
