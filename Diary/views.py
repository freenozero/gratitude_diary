from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate, get_user_model
from .forms import UserCreationForm, LoginForm
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
    if request.method == 'POST':
        login_form = LoginForm(request.POST)

        if login_form.is_valid():
            email = login_form.cleaned_data['email']
            password = login_form.cleaned_data['password']

            user = authenticate(
                email=email,
                password=password
            )
            if user is not None:
                login(request, user)
            else:
                login_form.add_error(None, '아이디 또는 비밀번호가 올바르지 않습니다')
    else:
        login_form = LoginForm()
    context = {
        'login_form': login_form,
    }
    return render(request, 'index.html', context)


def login_view(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)

        if login_form.is_valid():
            email = login_form.cleaned_data['email']
            password = login_form.cleaned_data['password']

            user = authenticate(
                email=email,
                password=password
            )
            if user is not None:
                login(request, user)
            else:
                login_form.add_error(None, '아이디 또는 비밀번호가 올바르지 않습니다')
    else:
        login_form = LoginForm()
    context = {
        'login_form': login_form,
    }
    return render(request, 'index.html', context)

def logout_view(request):
    logout(request)
    return redirect('login_view')

def user(request):
    return render(request, 'user.html')
