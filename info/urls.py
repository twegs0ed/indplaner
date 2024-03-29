
from django.urls import path
from . import views

urlpatterns = [
    path('', views.info, name='info_info'),
    path('gantt', views.gantt, name='info_gantt'),
    #path('<int:pk>/', views.tool_detail, name='tool_detail'),
] 