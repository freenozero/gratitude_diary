from django.urls import path, include
from . import views

#app_name = 'Diary'
urlpatterns = [
    path('', views.login_view, name='index'),
    path('user/', views.user, name='user'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('signout/', views.signOut_view, name='signOut'),
]
