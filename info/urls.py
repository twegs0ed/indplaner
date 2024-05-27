
from django.urls import path
from . import views

urlpatterns = [
    path('', views.info, name='info_info'),
    path('gantt', views.gantt, name='info_gantt'),
    path('report', views.report, name='info_report'),
    path('stock', views.stock, name='info_stock'),
    #path('<int:pk>/', views.tool_detail, name='tool_detail'),
] 