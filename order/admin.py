from django.contrib import admin
from .models import Order, Firm, Orderformed
from import_export.admin import ExportActionMixin, ImportExportModelAdmin
from import_export import resources
from tools.models import Toolsonwarehouse
from django.contrib.admin.models import LogEntry

#Меняем статус заказа на  заказано
def make_ordered(modeladmin, request, queryset):
    count_minus(queryset)
    queryset.update(status= Order.ORDERED)
make_ordered.short_description = "Статус заказано"

#Меняем статус заказа на оплачен
def make_payed(modeladmin, request, queryset):
    count_minus(queryset)
    queryset.update(status= Order.PAYED)
make_payed.short_description = "Статус оплачено"

#Меняем статус заказа на "получен"
def make_com(modeladmin, request, queryset):
    count_plus(queryset)
    queryset.update(status= Order.COM)
make_com.short_description = "Статус получено"

#Меняем статус заказа на закзаан рабочим
def make_ordered_by_worker(modeladmin, request, queryset):
    count_minus(queryset)
    queryset.update(status= Order.ORDERED_BY_WORKER)
make_ordered_by_worker.short_description = "Статус заявка от рабочего"

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


class OrderResource(resources.ModelResource):

    class Meta:
        model = Order

        fields = ('tool__title', 'count', 'worker__bio', 'worker__workplace__name')
        export_order = ('tool__title', 'count')
class OrderformedResource(resources.ModelResource):

    class Meta:
        model = Order

        fields = ('tools__title')
        #export_order = ('tool__title', 'count')


class FirmAdmin(admin.ModelAdmin):
    list_display = ('title', 'text')
    search_fields = ['title']
    ordering = ['title']
class OrderAdmin(ExportActionMixin, admin.ModelAdmin):
    resource_class = OrderResource
    list_display = ('tool', 'count', 'status', 'firm')
    list_filter = ('firm', 'status', 'worker')
    search_fields = ['tool__title', 'worker__bio']
    ordering = ['-order_date_worker','tool__title']
    autocomplete_fields = ['worker', 'tool']
    actions = [make_ordered, make_payed, make_com, make_ordered_by_worker]
    list_editable = ['firm', 'count']

class OrderformedAdmin( admin.ModelAdmin):
    resource_class = OrderformedResource
    list_display = ('get_tools','bill', 'datetime')
    list_display_links = ('datetime', )
    #search_fields = ['title']
    ordering = ['-datetime']
    search_fields = ['tools__tool__title', 'bill']

class LogEntryAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'action_time', 'user', 'content_type', 'object_repr', 'action_flag', 'change_message')
    list_filter = ('content_type',)
    search_fields = ['user__username',]
    date_hierarchy = 'action_time'
admin.site.register(LogEntry, LogEntryAdmin)

#admin.site.register(Firm, FirmAdmin)
admin.site.register(Order, OrderAdmin)
#admin.site.register(Orderformed, OrderformedAdmin)
