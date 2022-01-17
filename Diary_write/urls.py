from django.urls import path, include
from . import views
#app_name = 'Diary_write'
urlpatterns = [
    path('', views.main, name='main'),
    path('write/', views.Diary, name='Diary'),
]
