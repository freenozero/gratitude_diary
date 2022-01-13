from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('user/', views.user, name='user'),
    path('logout/', views.logout_view, name='logout_view'),
    path('withdrawal/', views.withdrawal, name='withdrawal')
]
