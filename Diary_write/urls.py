from django.urls import path, include
from . import views
#app_name = 'Diary_write'
urlpatterns = [
    path('', views.main, name='main'),
    path('MyDiary/', views.diary_view, name='Diary'),
    path('MyDiary/write/', views.write_view, name='DiaryWrite'),
    path('MyDiary/read/<int:diary_cnt>', views.read_view, name='DiaryRead'),
    path('MyDiary/edit/', views.edit_view, name='DiaryEdit')
]
