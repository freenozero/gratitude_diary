from django.urls import path, include
from . import views

#app_name = 'Diary'
urlpatterns = [
    path('', views.login_view, name='index'),
    path('user/', views.user, name='user'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout_view, name='logout_view'),
    path('signout/', views.signOut, name='signOut'),
    path('change_password/',views.change_password, name="re_password")
]
