from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib import auth
#
# def index(request):
#     if request.moethd == "POST":
#         username = request.POST["username"]
#         password = request.POST["password"]
#         user = authenticate(username = username, password = password)
#         notUser = "don't login" #로그인 실패시 문자
#         if user is not None:
#             #로그인 성공
#             login(request, username)
#             return render(request, 'user.html', {'username':username, 'password':password})
#         else:
#             #로그인 실패시 notUser 문자 반환
#             return render(request, {'notUser': notUser})
#     return render(request, 'index.html')

def index(request):
    return render(request, 'index.html')

def login(request):
    return render(request, 'login.html')


def signup(request):
    if request.method == "POST":
        if request.POST["password1"] == request.POST["password2"]:
            user = User.objects.create_user(username=request.POST["username"],
                                            password=request.POST["password1"])
            auth.login(request, user)
            return redirect('login')
        return render(request, 'signup.html')
    return render(request, 'signup.html')

def user_view(request):
    return render(request, 'user.html')