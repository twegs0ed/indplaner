
from django.urls import path
from . import views

urlpatterns = [
    path('add', views.add, name='work_add'),
    path('work/add/<int:id>/', views.add),
    path('detail', views.detail, name='detail'),
    #path('<int:pk>/', views.tool_detail, name='tool_detail'),
] 