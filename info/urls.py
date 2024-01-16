
from django.urls import path
from . import views
from .views import ToolAutocompleteView

urlpatterns = [
    path('', views.info, name='info_info'),
    path('gantt', views.gantt, name='info_gantt'),
    path('tool-autocomplete/', ToolAutocompleteView.as_view(), name='tool-autocomplete'),
    #path('<int:pk>/', views.tool_detail, name='tool_detail'),
] 