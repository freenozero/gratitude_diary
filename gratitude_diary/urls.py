from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('Diary.urls')),
    path('User/', include('Diary.urls')),
    path('Diary/', include('Diary_write.urls')),
    path('admin/', admin.site.urls),
]
