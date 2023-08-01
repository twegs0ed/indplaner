
from django.contrib import admin
from django.urls import include,path

admin.site.site_header = 'Учет инструмента'
admin.site.site_title = 'Учет инструмента'
admin.site.index_title = ''
urlpatterns = [
    #path('', include('tools.urls')),
    path('', admin.site.urls),
    path('tools/', include('tools.urls')),
    #path('admin/', admin.site.urls),

]

