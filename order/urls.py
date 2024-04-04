
from django.urls import path
from . import views

urlpatterns = [
    path('printmk', views.printmk, name='order_printmk'),
    path('printmk/<int:id>/', views.printmk),
    path('printmkall/<int:id>/', views.printmkall),
    path('printpr/<int:id>/', views.printpr),
    path('getouts', views.getouts, name='order_getouts'),
    path('getouts/<int:firm>/', views.getouts),
    path('priems', views.priems, name='order_priems'),
    path('priems/<int:firm>/', views.priems),
    #path('<int:pk>/', views.tool_detail, name='tool_detail'),
] 