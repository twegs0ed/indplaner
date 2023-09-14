
from django.urls import path
from . import views

urlpatterns = [
    path('', views.info, name='info_info'),
    #path('<int:pk>/', views.tool_detail, name='tool_detail'),
] 