from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect

def index(request):
    if request.moethd == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username = username, password = password)
        notUser = "don't login" #로그인 실패시 문자
        if user is not None:
            #로그인 성공
            login(request, username)
            return render(request, 'user.html', {'username':username, 'password':password})
        else:
            #로그인 실패시 notUser 문자 반환
            return render(request, {'notUser': notUser})
    return render(request, 'index.html')


def login(request):
    return render(request, 'login.html')


def logout(request):
    logout(request)
    return redirect('index.html')


def user_view(request):
    return render(request, 'user.html')