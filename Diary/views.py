from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, get_user_model
from .forms import UserCreationForm
User = get_user_model()

def signup(request):
    if request.method == "POST": #POST 방식일때
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save() #새로 만들어진 User의 DB를 저장.
            messages.success(request, "회원가입 됨")
            return redirect('/')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form' : form})


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
