from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.login_view, name='index'),
    path('signup/', views.signup, name='signup'),
    path('user/', views.user, name='user'),
    path('logout/', views.logout_view, name='logout_view'),
    path('signOut/', views.signout_view, name='signOut'),
    path('Diary/', views.Diary, name='Diary'),
    path('main/', views.main, name='main')
]
