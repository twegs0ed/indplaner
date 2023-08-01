from django.urls import path
from . import views

urlpatterns = [
    path('', views.tools_list, name='tools_list'),
    path('<int:pk>/', views.tool_detail, name='tool_detail'),
]