from django.urls import path, include
from . import views
#app_name = 'Diary_write'
urlpatterns = [
    path('', views.main, name='main'),
    path('MyDiary/', views.Diary_view, name='Diary'),
    path('DiaryWrite/', views.write_view, name='DiaryWrite'),
    path('DiaryEdit/', views.edit_view, name='DiaryEdit')
]
