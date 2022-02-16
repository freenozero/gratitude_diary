from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('Diary.urls')),
    path('Diary/', include('Diary_write.urls')),
    path('Diary_deco/', include('Diary_deco.urls')),
    path('admin/', admin.site.urls),
    # path('accounts/', include('allauth.urls')),

]
