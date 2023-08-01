from django.contrib import admin
from rangefilter.filters import DateRangeFilter, DateTimeRangeFilter
from .models import Toolsonwarehouse, Tools, Rec_Tools, Priem
from profiles.models import Profile
from order.models import Order
from import_export.admin import ExportActionMixin, ImportExportModelAdmin
from import_export import resources
from import_export.fields import Field
from django.utils.html import format_html
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

    period = Field(attribute='get_period',column_name='period')

    class Meta:
        model = Tools
        fields = ('tool__title', 'count','worker__bio')
        export_order = ('tool__title', 'worker__bio', 'count')


class ToolsonwarehouseAdmin(ExportActionMixin, admin.ModelAdmin):
    #autocomplete_fields = ['tool']
    readonly_fields = ('need_count',)
    list_display = ('id', 'title', 'count', 'min_count', 'need_count', 'count_deficite')
    search_fields = ['title']
    ordering = ['title']
    actions = [order_it]
    list_editable = ['title']

    def count_deficite(self, obj):
        i = Order.get_count_ordered(obj)
        if i>0 and i<(int(obj.min_count or 0)-int(obj.count or 0)):#Желтый
            result = format_html('<p style="background-color: #e3de46  ; color: #424746  ">'+str(i)+'('+str(int(obj.min_count or 0)-int(obj.count or 0)-int(i))+')</p>')
        elif i>=0 and i>=(int(obj.min_count or 0)-int(obj.count or 0)):#Зеленый
            result = format_html('<p style="background-color: #3ec76d ; color: #342ecf ">'+str(i)+'</p>')
        else:#красный
            result = format_html('<p style="background-color: #FF5656 ; color: #FFFBAF ">'+str(i)+'('+str(int(obj.min_count or 0)-int(obj.count or 0)-int(i))+')</p>')
        return result
    count_deficite.short_description = "заказано(не хватает)"

class ToolsAdmin(ExportActionMixin, admin.ModelAdmin):
    #raw_id_fields = ('worker', 'tool')
    autocomplete_fields = ['worker', 'tool']
    resource_class = ToolsResource
    list_display = ('worker', 'tool', 'count', 'giveout_date', 'get_period')
    list_filter = (('giveout_date', DateRangeFilter), 'worker')
    search_fields = ['tool__title', 'worker__bio']
    ordering = ['-giveout_date']

    pass
class Rec_ToolsAdmin(ExportActionMixin, admin.ModelAdmin):
    #raw_id_fields = ('worker', 'tool')
    autocomplete_fields = ['worker', 'tool']
    resource_class = ToolsResource
    list_display = ('worker', 'tool', 'count', 'giveout_date', 'get_period')
    list_filter = (('giveout_date', DateRangeFilter), 'worker')
    search_fields = ['tool__title', 'worker__bio']
    ordering = ['-giveout_date']
    pass
class ToolsdeficiteAdmin(admin.ModelAdmin):
    pass

class PriemAdmin(ExportActionMixin, admin.ModelAdmin):
    autocomplete_fields = ['tool']
    list_display = ('tool', 'count', 'giveout_date')
    #list_filter = (('giveout_date', DateRangeFilter))
    search_fields = ['tool__title']
    pass

admin.site.register(Tools, ToolsAdmin)
admin.site.register(Priem, PriemAdmin)
admin.site.register(Toolsonwarehouse, ToolsonwarehouseAdmin)
admin.site.register(Rec_Tools, Rec_ToolsAdmin)
