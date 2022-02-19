from django.urls import path, include
from . import views

#app_name = 'Diary_write'

urlpatterns = [
    path('', views.main, name='main'),
    path('MyDiary/', views.diary_view, name='Diary'),
    path('MyDiary/write/', views.write_view, name='DiaryWrite'),
    path('MyDiary/test/', views.test_write, name='DiarytestWrite'),
    path('MyDiary/read/', views.read_view, name='DiaryRead'),
    path('MyDiary/edit/<int:diary_cnt>', views.edit_view, name='DiaryEdit'),
    path('MyDiary/erase/<int:diary_cnt>', views.erase_view, name='DiaryErase'),
    path('decorate_note/',views.decorate_note, name= "decorate_note"),
]
