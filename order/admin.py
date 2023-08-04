from django.contrib import admin
from .models import Order, Firm, Orderformed
from import_export.admin import ImportExportModelAdmin
from import_export import resources
from tools.models import Toolsonwarehouse
from django.contrib.admin.models import LogEntry
from import_export.fields import Field
from import_export.widgets import ForeignKeyWidget

#Меняем статус заказа на  заказано
def make_ordered(modeladmin, request, queryset):
    count_minus(queryset)
    queryset.update(status= Order.ORDERED)
make_ordered.short_description = "Статус запущено"#заказано

#Меняем статус заказа на оплачен
def make_payed(modeladmin, request, queryset):
    count_minus(queryset)
    queryset.update(status= Order.PAYED)
make_payed.short_description = "Статус отдано на сторону"#оплачено

#Меняем статус заказа на "получен"
def make_com(modeladmin, request, queryset):
    count_plus(queryset)
    queryset.update(status= Order.COM)
make_com.short_description = "Статус изготовлено"#получено

#Меняем статус заказа на закзаан рабочим
def make_ordered_by_worker(modeladmin, request, queryset):
    count_minus(queryset)
    queryset.update(status= Order.ORDERED_BY_WORKER)
make_ordered_by_worker.short_description = "Статус в запуске"#заяввка

def count_minus(queryset):
    orderformed = Orderformed()
    orderformed.status = Order.ORDERED
    orderformed.save()
    for e in queryset.all():
        orderformed.tools.add(e)

    #Уменьшаем количество на складе, так как статус было получено
    if queryset.values()[0]['status'] == Order().COM:#если предыдущий статус был "получено"
        tool = Toolsonwarehouse.objects.get(id=queryset.values()[0]['tool_id'])
        tool.count = int(tool.count) - int(queryset.values()[0]['count'])#то количество инструмента на складе уменьшаем
        tool.save()

def count_plus(queryset):
    #Увеличиваем количество, так как статус было не получено
    if queryset.values()[0]['status'] != Order().COM:#если предыдущий статус был не "получено"
        tool = Toolsonwarehouse.objects.get(id=queryset.values()[0]['tool_id'])
        tool.count = int(tool.count) + int(queryset.values()[0]['count'])#то количество инструмента на складе уменьшаем
        tool.save()

class ForeignKeyWidgetWithCreation (ForeignKeyWidget):

    def clean(self, value, row=None, *args, **kwargs):
        try:
            return super(ForeignKeyWidgetWithCreation, self).clean(value, row, *args, **kwargs)
        except:
            return self.model.objects.create(**{self.field: value})
    

class OrderResource(resources.ModelResource):
    tool = Field(
        column_name='tool',
        attribute='tool',
        widget=ForeignKeyWidgetWithCreation(model=Toolsonwarehouse, field='title'))
    firm = Field(
        column_name='firm',
        attribute='firm',
        widget=ForeignKeyWidgetWithCreation(model=Firm, field='title'))
    class Meta:
        model = Order

        fields = ('tool', 'count','exp_date')
        export_order = ('tool', 'count')
        exclude = ('id',)
        import_id_fields = ('tool', 'count', 'firm','exp_date')


class FirmAdmin(admin.ModelAdmin):
    list_display = ('title', 'text')
    search_fields = ['title']
    ordering = ['title']
class OrderAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = OrderResource
    list_display = ('tool','count', 'status', 'firm','exp_date')
    list_filter = ('firm', 'status')
    search_fields = ['tool__title']
    ordering = ['tool__title']
    autocomplete_fields = [ 'tool']
    actions = [make_ordered, make_payed, make_com, make_ordered_by_worker]
    list_editable = ['firm', 'count']
    ordering = ['exp_date','tool']
    
    class Media:
        css = {
            'all': (
                'css/fancy.css',
            )
        }
        js = ('js/guarded_admin.js',)
    


class LogEntryAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'action_time', 'user', 'content_type', 'object_repr', 'action_flag', 'change_message')
    list_filter = ('content_type',)
    search_fields = ['user__username',]
    date_hierarchy = 'action_time'
admin.site.register(LogEntry, LogEntryAdmin)

admin.site.register(Firm, FirmAdmin)
admin.site.register(Order, OrderAdmin)
#admin.site.register(Orderformed, OrderformedAdmin)
