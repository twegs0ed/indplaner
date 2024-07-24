
from django.urls import path
from . import views

urlpatterns = [
    path('add', views.add, name='work_add'),
    path('work/addoptim/', views.addoptim, name='workoptim_add'),
    path('work/add/<int:id>/', views.add),
    path('workaddsclad/<int:id>/', views.addsclad),
    path('detail', views.detail, name='detail'),
    #path('<int:pk>/', views.tool_detail, name='tool_detail'),
] 