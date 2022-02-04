from django.urls import path, include
from . import views

#app_name = 'Diary_write'

urlpatterns = [
    path('', views.main, name='main'),
    path('MyDiary/', views.diary_view, name='Diary'),
    path('MyDiary/write/<int:year>/<int:month>/<int:day>', views.write_view, name='DiaryWrite'),
    path('MyDiary/read/<int:year>/<int:month>/<int:day>', views.read_view, name='DiaryRead'),
    path('MyDiary/edit/<int:diary_cnt>', views.edit_view, name='DiaryEdit'),
    path('MyDiary/erase/<int:diary_cnt>', views.erase_view, name='DiaryErase')
]
