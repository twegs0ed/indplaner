
from django.urls import path
from . import views

urlpatterns = [
    path('/printmk', views.printmk, name='order_printmk'),
    path('/printmk/<int:id>/', views.printmk),
    #path('<int:pk>/', views.tool_detail, name='tool_detail'),
] 