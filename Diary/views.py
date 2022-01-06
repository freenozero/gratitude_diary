from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib import auth


def signup(request):
    if request.method == "POST":
        if request.POST['password'] == request.POST['confirm']:
            user = User.objects.create_user(username=request.POST["username"],
                                            password=request.POST["password"])
            auth.login(request, user)
            return redirect('/')
    return render(request, 'signup.html')


def index(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)
        if user is not None:
            # 로그인 성공
            login(request, username)
            return render(request, 'user.html', {'username': username, 'password': password})
        else:
            # 로그인 실패시 notUser 문자 반환
            return render(request, 'index.html', {'notUser': True})
    return render(request, 'index.html')


# def index(request):
#     return render(request, 'index.html')
#
# def login(request):
#     return render(request, 'login.html')


def user(request):
    return render(request, 'user.html')
