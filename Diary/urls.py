from django.urls import path, include
from . import views

#app_name = 'Diary'
urlpatterns = [
    path('', views.login_view, name='index'),
    path('signup/', views.signups, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('signout/', views.signOut, name='signOut'),
    path('change_password/',views.change_password, name="re_password"),
    path('change_phonenum/', views.change_phonenum, name="re_phonenum"),
    path('main/',views.main, name='main'),
    path('activate/<str:uidb64>/<str:token>', views.activate, name='activate'),
    path('topmenu/', views.topmenu, name='topmenu'),
    path('userprofile/', views.userprofile, name='userprofile')

]
